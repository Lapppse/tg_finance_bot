import kb
from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Вітанне! Выберыце адно з дзеянняў у з’явіўшайся клавіятуры.",
        reply_markup=kb.start_kb,
    )
