from aiogram.dispatcher import FSMContext
from humanfriendly.terminal import ansi_width

from data.config import ADMINS
from loader import db,userdb,kinodb,dp,bot
from aiogram import types
from states.full_states import Deletekino,Kinodata,Reklmayoz,CaptionC
from keyboards.inline.inline_handler import reklama_uchun,reklama_qabul
"""Odan sinini korish"""
@dp.message_handler(commands="count1")
async def count_users_handler(message:types.Message):
    count=userdb.count_users()
    await message.answer(f"shuncha odam bor={count}")

"""Kinoki o'chirish """
@dp.message_handler(commands="delete")
async def kino_handler(msg:types.Message):
    await msg.answer("Kinoni raqamini kiriting: ")
    await Deletekino.kinokod.set()

@dp.message_handler(state=Deletekino.kinokod,content_types=types.ContentType.TEXT)
async def delete_handler(msg:types.Message,state:FSMContext):

    post_id=int(msg.text)
    try:
        await kinodb.delete_movie(post_id=post_id)
        for admins in ADMINS:
            await msg.answer(admins,"Kino uchirildi:")
            await state.finish()
    except ValueError:
        for admins in ADMINS:
            await msg.answer(admins,"Faqat raqam kiriting: ")


"""Kinoni sonini korish"""
@dp.message_handler(commands="kinoson")
async def kino_count_handler(msg:types.Message):
    son_kino= await kinodb.count_all_kinos()
    await msg.answer(f"Bor={son_kino}")


"""Reklamini yuborish """
@dp.message_handler(commands="reklama")
async def  start_reklama_handler(message:types.Message):
    await message.answer("Reklamani kiriting: ")
    await Reklmayoz.reklamayoz.set()

@dp.message_handler(state=Reklmayoz.reklamayoz)
async def reklama_handler(message:types.Message,state:FSMContext):
    reklamayoz=message.text
    await state.update_data(
        {
        "reklamayoz":reklamayoz
        }
    )

    rek_info = await state.get_data()
    reklama = rek_info.get("reklamayoz")


    info = f"here is you reklama"
    info+=f"here {reklama}"
    await bot.send_message(ADMINS[0],info,reply_markup=reklama_qabul)
    await message.delete()


@dp.callback_query_handler(state=Reklmayoz.reklamayoz,text="no")
async def back_1_handler(callback: types.CallbackQuery,state:FSMContext):
    await callback.message.delete()
    await state.finish()



@dp.callback_query_handler(state=Reklmayoz.reklamayoz, text="yes")
async def send_rek_handler(callback:types.CallbackQuery,state:FSMContext):
    await callback.message.delete()
    rek_info = await state.get_data()
    reklama = rek_info.get("reklamayoz")
    users = await userdb.select_all_users()
    for user in users:
        await callback.bot.send_message(user['telegram_id'], F"Bu reklama: {reklama}")


@dp.message_handler(commands="caption_search")
async def search_handler(message:types.Message):
    await message.answer("Caption yozing")
    await CaptionC.captionsearch.set()

@dp.message_handler(state=CaptionC.captionsearch)
async def caption_search_handler(message:types.Message,state:FSMContext):
    keywords=message.text
    try:
        result=await kinodb.search_kino_by_caption(keywords)

        if result:
            # Отправляем каждое видео
            for kino in result:
                file_id = kino['file_id']
                caption = kino['caption']
                post_id = kino["id"]
                await kinodb.increment_kino_views(post_id)
                if file_id:  # Проверяем, что file_id не пустой
                    try:
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=file_id,
                            caption=f"ID: {kino['id']}\nCaption: {caption}\nViews: {kino['views']}"
                        )
                    except Exception as e:
                        await message.answer(f"Video yuborishda xatolik: {e}")
                else:
                    await message.answer(f"Video topilmadi: file_id bo'sh.")
        else:
            await message.answer("Hech qanday kino topilmadi.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")




    await state.finish()
