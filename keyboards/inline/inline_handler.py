from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reklama_uchun=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Xa",callback_data="boladi"),
            InlineKeyboardButton("Yoq",callback_data="bolmaydi")
        ],
    ]
),
reklama_qabul=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Xa",callback_data="yes"),
            InlineKeyboardButton(text="Bekor qilish", callback_data="no")
        ]
    ]
)