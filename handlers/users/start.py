import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp,db,userdb,kinodb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    telegram_id=message.from_user.id
    username=message.from_user.username

    try:
        user=await userdb.add_user(telegram_id=telegram_id,username=username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await userdb.select_user(telegram_id=telegram_id)
    await message.answer("Xush kelibsiz botga")


"""
#Uyga  vazifa  


#userga  reklama yes 
#kinolar statistikasi no {get_most_viewed_kino}
#kino  qo'shish yes
#kino o'chirish yes
# kinoni  caption bo'yicha  qidiirsh yes {search_kino_by_caption}
# kinoni id  bo'yicha qidirish yes
# kinoni  update qilish  yes {update_kino_caption}
#userlar sonini aniqlash   statistika yes
#kinolar  sonini aniqlash  statistika yes
"""