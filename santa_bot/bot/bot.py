from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from santa_bot.db import db_manager
from santa_bot.db.tables import User
from santa_bot.utils import states, consts

dp = Dispatcher()
router = Router()
dp.include_router(router)


@dp.message(CommandStart())
async def welcome_message(message: Message, state: FSMContext):
    user = await db_manager.get_record(User, id=message.from_user.id)
    await state.clear()

    if not user:
        new_user = User(id=message.from_user.id, username=message.from_user.username)
        await db_manager.add_record(new_user)
        await state.set_state(states.NAME_EXPECTING_STATE)

        await message.answer(
            consts.NAME_REQUEST
        )

    else:
        await message.answer(
            consts.ALREADY_REGISTERED
        )


@router.message(states.NAME_EXPECTING_STATE)
async def handle_message(message: Message, state: FSMContext):
    await db_manager.update_record(message.from_user.id, name=message.text)

    await message.answer(
        consts.PRICE_REQUEST
    )

    await state.set_state(states.PRICE_EXPECTING_STATE)


@router.message(states.PRICE_EXPECTING_STATE)
async def handle_message(message: Message, state: FSMContext):
    await db_manager.update_record(message.from_user.id, wish_price=message.text)

    await message.answer(
        consts.WISH_REQUEST
    )

    await state.set_state(states.WISH_EXPECTING_STATE)


@router.message(states.WISH_EXPECTING_STATE)
async def handle_message(message: Message, state: FSMContext):
    await db_manager.update_record(message.from_user.id, wish_list=message.text)

    await message.answer(
        consts.FINAL_INFO
    )

    await state.clear()
