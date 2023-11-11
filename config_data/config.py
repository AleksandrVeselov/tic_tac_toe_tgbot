from dataclasses import dataclass
from environs import Env


@dataclass
class Tgbot:
    """Класс с настройками для телеграм-бота"""
    token: str  # Токен телеграм-бота


@dataclass
class Config:
    """Загрузка настроек бота"""
    tg_bot: Tgbot


def load_config(path: str | None=None) -> Config:
    """
    Загрузка настроек из переменных окружения
    :param path: путь до файла с переменными окружения
    :return: экземпляр класса Config c загруженными переменными
    """

    # создаем экземпляр класса Env
    env: Env = Env()

    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env(path)

    # создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return Config(tg_bot=Tgbot(token=env('BOT_TOKEN')))
