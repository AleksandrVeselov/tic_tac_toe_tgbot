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

users_dict = {}  # словарь пользователей


# Состояния, в которых может находиться бот
class FSMGame(StatesGroup):
    play_state = State()  # состояние "в игре"


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """Хэндлер срабатывает на команду /start в состоянии вне игры и присылает в чат стартовую клавиатуру."""

    # проверяем есть ли id пользователя в словаре users_dict, если нет добавляем его в словарь
    # и создаем ему экземпляр класса Game
    if message.from_user.id not in users_dict:
        users_dict[message.from_user.id] = Game()

    await message.answer(LEXICON['/start'], reply_markup=start_kb)  # отправляем в чат стартовое сообщение и клавиатуру


@router.message(F.text == 'Правила')
async def process_help_command(message: Message):
    """Хэндлер срабатывает на команду "Правила", присылает в чат правила игры и стартовую клавиатуру"""

    await message.answer(LEXICON['/help'])  # отправляем в чат сообщение по ключу help


@router.message(F.text == 'Не сейчас')
async def process_no_command(message: Message, state: FSMContext):
    """Хэндлер срабатывает на команду "Не сейчас", присылает в чат соответствующее сообщение и стартовую клавиатуру"""

    await message.answer(LEXICON['no'])  # отправляем в чат сообщение по ключу no
    await state.set_state(default_state)  # переводим бота в состояние по умолчанию


@router.message(F.text == 'Сыграем', StateFilter(default_state))
async def process_play_command(message: Message, state: FSMContext):
    """Хэндлер срабатывает на команду "Сыграем" в состоянии по умолчанию,
    формирует игровое поле и отправляет его в чат"""

    # проверяем есть ли id пользователя в словаре users_dict, если нет добавляем его в словарь
    # и создаем ему экземпляр класса Game
    if message.from_user.id not in users_dict:
        users_dict[message.from_user.id] = Game()

    game = users_dict[message.from_user.id]  # достаем из словаря по ключу нужный экземпляр класса Game
    game_keyboard = create_game_keyboard(game.game_field)  # создаем игровую клавиатуру

    # отправляем в чат сообщение по ключу start_game с игровой инлайн-клавиатурой
    await message.answer(LEXICON['start_game'], reply_markup=game_keyboard)

    await state.set_state(FSMGame.play_state)  # переводим бота в состояние "в игре"


@router.callback_query(lambda x: re.fullmatch('[012],[012]', x.data), StateFilter(FSMGame.play_state))
async def process_move_button_press(callback: CallbackQuery, state: FSMContext):
    """хэндлер срабатывает на строку с координатами нажатой инлайн-кнопки на игровом поле в состянии play_state"""

    game = users_dict[callback.from_user.id]  # достаем из словаря по ключу id нужный экземпляр класса Game

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
                await state.set_state(default_state)  # переводим бота в состоянии по умолчанию
                game.reload_field()  # сбрасываем состояние игрового поля

            # проверяем на ничью
            elif game.is_board_full():
                await callback.message.edit_text(text='Победила дружба!!!',
                                                 reply_markup=game_keyboard)  # Отправляем ответ в чат
                await state.set_state(default_state)  # # переводим бота в состоянии по умолчанию
                game.reload_field()  # сбрасываем состояние игрового поля

            # в остальных случаях отправляем в чат соответствующее сообщение
            else:
                await callback.message.edit_text(text='Ты успешно сделал ход!!',
                                                 reply_markup=game_keyboard)

        # если клетка занята, отправляем чат соответствующее сообщение
        else:
            if callback.message.text != 'Клетка уже занята, выбери другую!':
                await callback.message.edit_text(text='Клетка уже занята, выбери другую!',
                                                 reply_markup=callback.message.reply_markup)

    # Если очередь компьютера, отправляем в чат соответствующее сообщение
    else:
        if callback.message.text != 'Сейчас не твоя очередь, нажми на кнопку "Ход компьютера"':
            await callback.message.edit_text(text='Сейчас не твоя очередь, нажми на кнопку "Ход компьютера"',
                                             reply_markup=callback.message.reply_markup)

    await callback.answer()


@router.callback_query(F.data == 'computer_move', StateFilter(FSMGame.play_state))
async def process_computer_move(callback: CallbackQuery, state: FSMContext):
    """хэндлер реагирует на нажатие инлайн-кнопки computer_move в состоянии play_state"""

    game = users_dict[callback.from_user.id]  # # достаем из словаря по ключу id нужный экземпляр класса Game
    move = game.computer_move()  # просчет хода компьютера
    game.make_move(game.computer_letter, move)  # делаем ход
    game.queue_flag = game.human_letter  # меняем флаг очереди на ход компьютера
    game_keyboard = create_game_keyboard(game.game_field)  # создаем инлайн-клавиатуру из игровой матрицы

    # проверяем есть на поле выигрышная ситуация
    if game.is_winner(game.computer_letter):
        await callback.message.edit_text(text='Я победил, ура!!!',
                                         reply_markup=game_keyboard)  # Отправляем ответ в чат
        await state.set_state(default_state)  # переводим бота в состояние по умолчанию
        game.reload_field()  # сбрасываем состояние игрового поля

    # проверяем на ничью
    elif game.is_board_full():
        await callback.message.edit_text(text='Победила дружба!!!',
                                         reply_markup=game_keyboard)  # Отправляем ответ в чат
        await state.set_state(default_state)  # переводим бота в состояние по умолчанию
        game.reload_field()  # сбрасываем состояние игрового поля

    # в остальных случаях
    else:
        await callback.message.edit_text(text='Я сделал ход, теперь ты',
                                         reply_markup=game_keyboard)

    await callback.answer()


@router.callback_query(lambda x: re.fullmatch('[012],[012]', x.data), StateFilter(default_state))
async def process_push_button_exit_state(callback: CallbackQuery):
    """хэндлер срабатывает на строку с координатами нажатой инлайн-кнопки на игровом поле в состоянии по умолчанию"""

    await callback.message.answer(LEXICON['/start'], reply_markup=start_kb)
    await callback.answer()


@router.callback_query(F.data == 'computer_move', StateFilter(default_state))
async def process_push_button_exit_state(callback: CallbackQuery):
    """хэндлер реагирует на нажатие инлайн-кнопки computer_move в состоянии по умолчанию"""

    await callback.message.answer(LEXICON['/start'], reply_markup=start_kb)
    await callback.answer()
