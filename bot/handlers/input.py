from datetime import date

import kb
from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import Conn
from loguru import logger
from utils import config

router = Router()


class ManualInputState(StatesGroup):
    money = State()
    desc = State()
    confirm = State()


@router.message(F.text == "Новы запіс")
async def expenses_input(message: types.Message):
    await message.reply("Hello", reply_markup=kb.input_kb)
    logger.info(f"user {message.from_user.id} used expenses_input command")
    return


@router.callback_query(StateFilter(None), F.data == "input_auto")
async def auto_input(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Функцыя знаходзіцца ў распрацоўцы.", True)
    logger.info(f"user {callback.from_user.id} used auto_input command")
    raise NotImplementedError


@router.callback_query(StateFilter(None), F.data == "input_manual")
async def manual_input(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Увядзіце вытрачаную суму грошай")
    await state.set_state(ManualInputState.money)
    logger.info(f"user {callback.from_user.id} started manual_input command")


@router.message(ManualInputState.money)
async def manual_input_money(message: types.Message, state: FSMContext):
    money = 0.0
    try:
        money = round(float(message.text.strip()), 2)
    except ValueError:
        await message.reply(
            'Дапускаюцца толькі лічбавыя значэнні з кропкай тыпу "15.83". Увядзіце карэктнае значэнне.'
        )
        return
    if money > 10000000:
        await message.reply(
            "Дапускаюцца значэнні не болей дзесяці мільёнаў. Увядзіце карэктнае значэнне."
        )
        return

    await state.set_data({"money": money, "desc": None})
    data = await state.get_data()
    desc = data["desc"]

    await state.set_state(ManualInputState.confirm)
    await message.answer(
        f"Дадзеныя:\nУведзеная сума: {money} рублёў\nУведзенае апісанне: {'няма' if desc is None else desc}",
        reply_markup=kb.input_confirm_kb,
    )
    logger.debug(money)
    logger.info(f"user {message.from_user.id} used manual_input_money command")


@router.callback_query(ManualInputState.confirm, F.data == "input_manual_change_money")
async def manual_input_change_money(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Увядзіце новую колькасць грошай")
    await state.set_state(ManualInputState.money)
    logger.info(
        f"user {callback.from_user.id} used manual_manual_input_change_money command"
    )


@router.callback_query(ManualInputState.confirm, F.data == "input_manual_desc")
async def manual_inputting_description(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.set_state(ManualInputState.desc)
    await callback.message.answer("Увядзіце апісанне (макс. 50 сімвалаў)")
    await callback.answer()
    logger.info(
        f"user {callback.from_user.id} used manual_inputting_description command"
    )


@router.message(ManualInputState.desc)
async def manual_input_description(message: types.Message, state: FSMContext):
    desc = message.text[:50]

    data = await state.get_data()
    await state.set_data({"money": data["money"], "desc": desc})
    await state.set_state(ManualInputState.confirm)
    await message.answer(
        f"Дадзеныя:\nУведзеная сума: {data['money']} рублёў\nУведзенае апісанне: {'няма' if desc is None else desc}",
        reply_markup=kb.input_confirm_kb,
    )
    logger.info(f"user {message.from_user.id} used manual_input_description command")


@router.callback_query(ManualInputState.confirm, F.data == "input_manual_confirm")
async def manual_input_confirm(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    with Conn(config.current_db_path) as db:
        db.execute(
            "INSERT INTO expenses (user_id, money, desc, date) VALUES (?,?,?,?)",
            (
                callback.from_user.id,
                int(data["money"] * 100),
                data["desc"],
                date.today(),
            ),
        )
    await state.clear()
    await callback.message.reply("Дадзеныя даданы.")
    await callback.answer()
    logger.info(f"user {callback.from_user.id} used manual_input_confirm command")
