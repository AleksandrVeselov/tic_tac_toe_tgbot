import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery

from keyboards.game_keyboard import create_game_keyboard
from keyboards.keyboard import start_kb
from lexicon.lexicon import LEXICON
from services.services import Game

router = Router()
game = Game()  # инициализируем игру


# Состояния, в которых может находиться бот
class FSMGame(StatesGroup):
    play_state = State()  # состояние "в игре"


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """Хэндлер срабатывает на команду /start в состянии вне игры и присылает в чат стартовую клавиатуру.
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['/start'], reply_markup=start_kb)


@router.message(F.text == 'Правила')
async def process_help_command(message: Message):
    """Хэндлер срабатывает на команду "Правила", присылает в чат правила игры и стартовую клавиатуру
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['/help'])


@router.message(F.text == 'Не сейчас')
async def process_no_command(message: Message, state: FSMContext):
    """Хэндлер срабатывает на команду "Не сейчас", присылает в чат соответствующее сообщение и стартовую клавиатуру
    Команды, которые может ввести пользователь на данном этапе: Правила, Не сейчас, Сыграем, любая другая команда"""
    await message.answer(LEXICON['no'])
    await state.set_state(FSMGame.exit_state)  # переводим бота в состояние вне игры


@router.message(F.text == 'Сыграем', StateFilter(default_state))
async def process_play_command(message: Message, state: FSMContext):
    """Хэндлер срабатывает на команду "Сыграем" в состоянии по умолчанию,
    формирует игровое поле и отправляет его в чат"""

    game_keyboard = create_game_keyboard(game.game_field)
    await message.answer(LEXICON['start_game'], reply_markup=game_keyboard)

    await state.set_state(FSMGame.play_state)  # переводим бота в состояние "в игре"


@router.callback_query(lambda x: re.fullmatch('[012],[012]', x.data), StateFilter(FSMGame.play_state))
async def process_move_button_press(callback: CallbackQuery, state: FSMContext):

    # Если очередь игрока
    if game.queue_flag == 1:
        move = (int(callback.data[0]), int(callback.data[2]))  # координаты нажатой инлайн-кнопки

        # Проверка свободна ли клетка, на которую нажал игрок
        if game.is_space_free(move):
            game.make_move(game.human_letter, move)  # делаем ход
            game.queue_flag = game.computer_letter  # меняем флаг очереди
            game_keyboard = create_game_keyboard(game.game_field)  # создаем новую инлайн-клавиатуру из игровой матрицы

            # проверяем есть на поле выигрышная ситуация
            if game.is_winner(game.human_letter):
                await callback.message.edit_text(text='Ты победил, поздравляю!!!',
                                                 reply_markup=game_keyboard)  # Отправляем ответ в чат
                await state.set_state(default_state)

            # проверяем на ничью
            elif game.is_board_full():
                await callback.message.edit_text(text='Победила дружба!!!',
                                                 reply_markup=game_keyboard)  # Отправляем ответ в чат
                await state.set_state(default_state)

            # в остальных случаях
            else:
                await callback.message.edit_text(text='Ты успешно сделал ход!!',
                                                 reply_markup=game_keyboard)  # Отправляем ответ в чат

        else:
            await callback.message.edit_text(text='Клетка уже занята, выбери другую!',
                                             reply_markup=callback.message.reply_markup)

    # Если очередь компьютера
    else:
        await callback.message.edit_text(text='Сейчас не твоя очередь, нажми на кнопку "Ход компьютера"',
                                         reply_markup=callback.message.reply_markup)

    await callback.answer()


@router.callback_query(F.data == 'computer_move', StateFilter(FSMGame.play_state))
async def process_computer_move(callback: CallbackQuery, state: FSMContext):
    move = game.computer_move()
    game.make_move(game.computer_letter, move)
    game.queue_flag = game.human_letter
    game_keyboard = create_game_keyboard(game.game_field)

    # проверяем есть на поле выигрышная ситуация
    if game.is_winner(game.computer_letter):
        await callback.message.edit_text(text='Я победил, ура!!!',
                                         reply_markup=game_keyboard)  # Отправляем ответ в чат
        await state.set_state(default_state)

    # проверяем на ничью
    elif game.is_board_full():
        await callback.message.edit_text(text='Победила дружба!!!',
                                         reply_markup=game_keyboard)  # Отправляем ответ в чат
        await state.set_state(default_state)

    # в остальных случаях
    else:
        await callback.message.edit_text(text='Я сделал ход, теперь ты',
                                         reply_markup=game_keyboard)

    await callback.answer()


@router.callback_query(lambda x: re.fullmatch('[012],[012]', x.data), StateFilter(default_state))
async def process_push_button_exit_state(callback: CallbackQuery):
    await callback.message.answer(LEXICON['/start'], reply_markup=start_kb)

    await callback.answer()


@router.callback_query(F.data == 'computer_move', StateFilter(default_state))
async def process_push_button_exit_state(callback: CallbackQuery):
    await callback.message.answer(LEXICON['/start'], reply_markup=start_kb)

    await callback.answer()
