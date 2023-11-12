import re

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.game_keyboard import create_game_keyboard
from keyboards.keyboard import start_kb
from lexicon.lexicon import LEXICON
from services.services import game_filed, computer_move, make_move

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """Хэндлер срабатывает на команду /start и присылает в чат стартовую клавиатуру.
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['/start'], reply_markup=start_kb)


@router.message(F.text == 'Правила')
async def process_help_command(message: Message):
    """Хэндлер срабатывает на команду "Правила", присылает в чат правила игры и стартовую клавиатуру
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['/help'])


@router.message(F.text == 'Не сейчас')
async def process_no_command(message: Message):
    """Хэндлер срабатывает на команду "Не сейчас", присылает в чат соответствующее сообщение и стартовую клавиатуру
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['no'])


@router.message(F.text == 'Сыграем')
async def process_play_command(message: Message):
    """Хэндлер срабатывает на команду "Сыграем", формирует игровое поле и отправляет его в чат"""
    game_keyboard = create_game_keyboard(game_filed)
    await message.answer(LEXICON['start_game'], reply_markup=game_keyboard)


@router.callback_query(lambda x: re.fullmatch('[012],[012]', x.data))
async def process_move_button_press(callback: CallbackQuery):

    # Проверка свободна ли клетка, на которую нажал игрок
    if game_filed[int(callback.data[0])][int(callback.data[2])] == 0:
        game_filed[int(callback.data[0])][int(callback.data[2])] = 1
        game_keyboard = create_game_keyboard(game_filed)
        await callback.message.edit_text(text='Ты успешно сделал ход!!',
                                         reply_markup=game_keyboard)

    else:
        await callback.message.edit_text(text='Клетка уже занята, выбери другую!',
                                         reply_markup=callback.message.reply_markup)

    await callback.answer()


@router.callback_query(F.data == 'computer_move')
async def process_computer_move(callback: CallbackQuery):
    move = computer_move(game_filed)
    make_move(game_filed, 2, move)
    game_keyboard = create_game_keyboard(game_filed)
    await callback.message.edit_text(text='Я сделал ход, теперь ты',
                                     reply_markup=game_keyboard)

    await callback.answer()
