from aiogram import types

start_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Новы запіс")],
        [types.KeyboardButton(text="Расходы")],
        [types.KeyboardButton(text="Графікі")],
    ],
    resize_keyboard=True,
)
