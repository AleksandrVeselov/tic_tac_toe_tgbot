from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from lexicon.lexicon import LEXICON

button_yes = KeyboardButton(text=LEXICON['yes_button'])
button_no = KeyboardButton(text=LEXICON['no_button'])
button_help = KeyboardButton(text=LEXICON['help_button'])


# Создаем клавиатуру с кнопками "Сыграем", "Не сейчаc" и "Правила"
start_kb = ReplyKeyboardMarkup(keyboard=[[button_yes, button_no, button_help]],
                               resize_keyboard=True,
                               one_time_keyboard=True)
