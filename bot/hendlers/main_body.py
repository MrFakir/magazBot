import asyncio
import os
from datetime import date

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from Config import BASE_DIR
from backend.create_user import login, create_user
from backend.validators import validate_id, get_clean_user_data
from bot.hendlers.registration_or_login_2 import RegistrationOrLoginStates
from bot.keyboards.for_registration import send_phone_number, next_button, cry_button
from bot.keyboards.for_main_body import main_menu_kb, today_button
from parser_id.bot_for_pars_id import send_user_id

router = Router()


class MainStates(StatesGroup):
    input_flight = State()


@router.message(RegistrationOrLoginStates.logged_in, F.text.lower() == 'далее')
async def main_menu(message: Message):
    await message.answer(
        text='Выберете чтобы вы хотели сделать',
        reply_markup=main_menu_kb()
    )


@router.message(RegistrationOrLoginStates.logged_in, F.text.lower() == 'ввести данные по рейсу')
async def main_menu(message: Message, state: FSMContext):
    await message.answer(
        text='Введите дату рейса по UTC (весь бот работает в UTC) \n'
             'Или нажмите кнопку "Сегодня"',
        reply_markup=today_button()
    )
    await state.set_state(MainStates.input_flight)


@router.message(MainStates.input_flight, F.text.lower() == 'сегодня (по utc)')
async def main_menu(message: Message, state: FSMContext):
    await message.answer(
        text=f'Текущая дата (по UTC) - {date.today()}',
        # запись в файл
        reply_markup=today_button()
    )


@router.message(MainStates.input_flight, F.text.lower())
async def main_menu(message: Message, state: FSMContext):
    await message.answer(
        text='Введите дату рейса по UTC \n'
             'в формате ДД.ММ.ГГ например 08.07.23 \n'
             'Или нажмите кнопку "Сегодня"',
        reply_markup=today_button()
    )
    # обработка и валидация даты и рейса, отправка его по новой
    # если валидация не пройдена, а если пройдена запись в файл
    # т.е. по условию мы смотрим, введенный текст соответствует дате или рейсу, и если чему либо соответствует, то
    # записываем соответствующие данные, сообщая об этом пользователю и ждём данные дальше
    await message.answer(
        text='Дата записана, введите номер рейса без U6 \n'
             'Если вы ошиблись с датой, можете её набрать снова.',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(RegistrationOrLoginStates.logged_in, F.text.lower())
async def main_menu(message: Message):
    await message.answer(
        text='Пожалуйста следуйте текущей инструкциям',
        reply_markup=main_menu_kb()
    )


def main():
    pass


if __name__ == '__main__':
    main()
