from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.keyboard import start_kb
from lexicon.lexicon import LEXICON

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'], reply_markup=start_kb)