from typing import Any, Dict
from aiogram import html

from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    print(data)
    text = f"asdf"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
