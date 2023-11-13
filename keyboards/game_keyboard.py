from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_game_keyboard(game_field: list[[list[int]]]) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры с кнопками, соответствующими переданному в нее списку с игровым полем
    :param game_field: список игрового поля
    :return: InlineKeyboardMarkup
    """
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()

    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # наполняем клавиатуру кнопками в соответствии с переданной матрицей
    for i in range(3):
        for j in range(3):

            if game_field[i][j] == 1:
                letter = 'X'
            elif game_field[i][j] == 2:
                letter = 'O'
            else:
                letter = game_field[i][j]

            buttons.append((InlineKeyboardButton(text=letter,
                                                 callback_data=f'{i},{j}')))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=3)
    kb_builder.row(InlineKeyboardButton(text='Ход компьютера', callback_data='computer_move'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
