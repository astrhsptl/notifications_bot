import logging
from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from states.notifications import Notification
from utils.notifications import show_summary

form_router = Router()



@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("new"))
async def new_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Notification.description)
    await message.answer(
        "Let's type notificatin description",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Notification.description)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Notification.is_periodic)
    await message.answer(
        f"Notification will be periodic?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Notification.is_periodic)
async def process_language(message: Message, state: FSMContext) -> None:
    await state.update_data(is_periodic=message.text)
    await state.set_state(Notification.date)
    await message.answer(
        "Let's type data (like 12.12.2012 12:12:12)",
    )

@form_router.message(Notification.date)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(date=message.text)
    await state.clear()
    await show_summary(message=message, data=data)