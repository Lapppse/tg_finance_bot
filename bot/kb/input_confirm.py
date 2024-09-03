from aiogram import types

input_confirm_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Пацвердзіць", callback_data="input_manual_confirm"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Змяніць суму", callback_data="input_manual_change_money"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Змяніць апісанне (апцыянальна)", callback_data="input_manual_desc"
            )
        ],
    ],
)
