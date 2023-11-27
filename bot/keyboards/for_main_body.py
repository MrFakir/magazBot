from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ввести данные по рейсу")
    kb.button(text="Просмотреть свои результаты")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def today_button() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Сегодня (по UTC)")
    return kb.as_markup(resize_keyboard=True)


# def send_phone_number() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardBuilder()
#     kb.button(text="Предоставить номер телефона", request_contact=True)
#     return kb.as_markup(resize_keyboard=True)


# def next_button() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardBuilder()
#     kb.button(text="Далее")
#     return kb.as_markup(resize_keyboard=True)


def main():
    pass


if __name__ == '__main__':
    main()
