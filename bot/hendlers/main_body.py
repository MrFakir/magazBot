import asyncio
import json
import os
from datetime import date

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from Config import BASE_DIR
from backend.create_user import login, create_user
from backend.validators import validate_id, get_clean_user_data, validate_date, validate_flight, \
    validate_undefined_flight
from bot.hendlers.registration_or_login_2 import RegistrationOrLoginStates
from bot.keyboards.for_registration import send_phone_number, next_button, cry_button
from bot.keyboards.for_main_body import main_menu_kb, today_button
from parser_id.bot_for_pars_id import send_user_id

router = Router()


class MainStates(StatesGroup):
    input_flight_date = State()
    input_flight_number = State()


@router.message(RegistrationOrLoginStates.logged_in, F.text.lower() == 'далее')
async def main_menu(message: Message):
    await message.answer(
        text='Выберете чтобы вы хотели сделать',
        reply_markup=main_menu_kb()
    )


@router.message(RegistrationOrLoginStates.logged_in, F.text.lower() == 'ввести данные по рейсу')
async def input_flight_date(message: Message, state: FSMContext):
    await message.answer(
        text='Введите дату рейса по UTC (весь бот работает в UTC) \n'
             'в формате ДД.ММ.ГГ например 08.07.23 \n'
             'Или нажмите кнопку "Сегодня"',
        reply_markup=today_button()
    )
    await state.set_state(MainStates.input_flight_date)


@router.message(MainStates.input_flight_date, F.text.lower() == 'сегодня (по utc)')
async def input_flight_date_today(message: Message, state: FSMContext):
    await message.answer(
        text=f'Текущая дата (по UTC) - {date.today()}',
        # запись в файл
        reply_markup=today_button()
    )
    await message.answer(
        text="Введите номер рейса, без U6 \n"
             "Например рейс U6300, нужно написать как 300 (Шутка про тракториста!) \n"
             "Если у Вас был разворотный рейс, введите какой-нибудь ОДИН номер рейса",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainStates.input_flight_number)


@router.message(MainStates.input_flight_date, F.text.lower())
async def input_flight_date_check(message: Message, state: FSMContext):
    result_valid, valid_data = validate_date(message.text)
    if result_valid:
        # Опять преобразовываю дату к строке, т.к. данными хочу обмениться через файл, хз как лучше...
        # некрасиво, потому что перед записью в базу, нужно будет опять превратить в date, т.к.
        # считаю, что хранить в базе дату в формате date - лучшее решение
        user_data = {'flight_date': str(valid_data)}
        with open(os.path.join(BASE_DIR, 'data', f'user_flight_{str(message.from_user.id)}.json'), 'w') as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)
        await message.answer(
            text="Дата записана"
        )
        await message.answer(
            text="Введите номер рейса, без U6 \n"
                 "Например рейс U6300, нужно написать как 300 (Шутка про тракториста!) \n"
                 "Если у Вас был разворотный рейс, введите какой-нибудь ОДИН номер рейса",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(MainStates.input_flight_number)
    else:
        await message.answer(
            text='Неверный формат даты! \n'
                 f'{valid_data} \n'
                 'Или нажмите кнопку "Сегодня"',
            reply_markup=today_button()
        )
        return


@router.message(MainStates.input_flight_number, F.text.lower())
async def input_flight_number(message: Message, state: FSMContext):
    result_valid, valid_data = validate_flight(message.text)
    if result_valid:
        await message.answer(
            text="ок...",
        )
        pass
    else:
        await message.answer(
            text=valid_data,
        )
        await message.answer(
            text="Введите номер рейса, без U6 \n"
                 "Например рейс U6300, нужно написать 300 (Шутка про тракториста!) \n"
                 "Если у Вас был разворотный рейс, введите какой-нибудь ОДИН номер рейса",
            reply_markup=ReplyKeyboardRemove()
        )
        with open(os.path.join(BASE_DIR, 'data', 'user_flight_number_error_log.json'), 'r') as file:
            flight_error_log = json.load(file)
        try:
            user_errors = flight_error_log[str(message.from_user.id)]
        except KeyError:
            flight_error_log[str(message.from_user.id)] = 1
        if flight_error_log[str(message.from_user.id)] < 5:
            flight_error_log[str(message.from_user.id)] += 1
            with open(os.path.join(BASE_DIR, 'data', 'user_flight_number_error_log.json'), 'w') as file:
                json.dump(flight_error_log, file, indent=4, ensure_ascii=False)
            return
        else:
            result_valid, valid_data = validate_undefined_flight(message.text)
            if result_valid:
                # запись рейса в базу
                await message.answer(
                    text="А вы настырные, возможно у меня нет этого рейса в базе, я запишу именно этот рейс в базу, "
                         "а отчёт об ошибки отправлю админу, и позже подгружу направления самостоятельно и "
                         "обновлю базу",
                    reply_markup=ReplyKeyboardRemove()
                )
                #функция записи в лог ошибки
                flight_error_log[str(message.from_user.id)] = 0
            else:
                await message.answer(text=valid_data)
                return


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
