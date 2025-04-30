from aiogram.dispatcher import FSMContext

from loader import db,userdb,kinodb,dp,bot
from aiogram import types
from states.full_states import Deletekino,Kinodata,Updatakino



@dp.message_handler(commands="kinoadd")
async def kino_add_function(msg:types.Message):
    await msg.answer("Kinoni yuboring")
    await Kinodata.kino.set()

@dp.message_handler(state=Kinodata.kino,content_types=types.ContentType.VIDEO)
async def kino_add_content(msg:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data["file_id"]=msg.video.file_id
        data["caption"]=msg.caption or "Kino"
    await msg.answer("kinuchun kod kiriting:")
    await Kinodata.number.set()

@dp.message_handler(state=Kinodata.number,content_types=types.ContentType.TEXT)
async def kod_handler(msg:types.Message,state:FSMContext):
    try:
        post_id=int(msg.text)
        async with state.proxy() as data:
            data["post_id"]=post_id
            await kinodb.add_kino(
                post_id=data["post_id"],
                file_id=data["file_id"],
                caption=data["caption"],
            )
        await msg.answer("Kino saqlandi:")
        await state.finish()
    except ValueError:
        await msg.answer("kino raqamini kiriting faqat raqam bolsin:")

@dp.message_handler(lambda message:message.text.isdigit())
async def kino_find_handler(msg:types.Message):
    if msg.text.isdigit():
        post_id=int(msg.text)
        data=await kinodb.get_kino_by_post_id(post_id=post_id)
        if data:
            file_id = data['file_id']
            caption = data['caption']
            # post_id = data["post_id"]
            try:
                await kinodb.increment_kino_views(post_id)
                await bot.send_video(chat_id=msg.from_user.id,
                                     video=data["file_id"],
                                     # caption=data["caption"],
                                     caption=f"ID:Caption: {caption}\nViews: {data['views']}"
                                     )
            except:
                await msg.answer("kino topilmadi xatolik qayta urinib koring")
        else:
            await msg.answer("Kino topilmadi")
    else:
        await msg.answer("Kino uchun raqamni kiriting: ")

@dp.message_handler(commands="update_kino")
async def kinoid_handler(message:types.Message):
    await message.answer("Kinoni id kiriting: ")
    await Updatakino.kinokod.set()

@dp.message_handler(state=Updatakino.kinokod)
async def kino_post_id_handler(message:types.Message,state:FSMContext):
    try:
        post_id=int(message.text)
        await state.update_data(post_id=post_id)
        await message.answer("Yangi caption kiriting")
        await Updatakino.updatakino.set()
    except ValueError:
        await message.answer("Kino ID sini kiriting Qaytatan kiriting raqamni:) ")

@dp.message_handler(state=Updatakino.updatakino)
async def new_caption_handler(message:types.Message,state:FSMContext):
    new_caption=message.text
    data=await  state.get_data()
    post_id=data.get("post_id")

    try:
        await kinodb.update_kino_caption(post_id=post_id,new_caption=new_caption)
        await message.answer(f"Post ID {post_id} uchun caption muvaffaqiyatli yangilandi!")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

    await state.finish()

