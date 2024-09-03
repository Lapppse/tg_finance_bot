from aiogram import types

input_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Увесці ўручную", callback_data="input_manual"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="Сканаванне чэка", callback_data="input_auto"
            ),
        ],
    ],
)
