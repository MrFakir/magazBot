import asyncio
import os
import time

from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from Config import BASE_DIR
from bot.keyboards.for_registration import get_registration_kb, send_phone_number, next_button

from backend.validators import validate_id
from backend.create_user import login, create_user
from parser_id.bot_for_pars_sender import send_user_id

router = Router()

qweqwe = 1


class RegistrationOrLoginStates(StatesGroup):
    input_phone_registration = State()
    input_id_registration = State()
    input_phone_login = State()
    input_id_login = State()
    send_phone = State()
    logged_in = State()


# переделка регистрации
# получаем номер телефона, ищем его в моей базе, если его в базе нет, то тогда прошу ввести табельный
# и только после этого иду стучаться для получения связки номер - табельны и регистрации нового пользователя
# ИЛИ
# анонимная регистрация на основании id юзера телеграмма, как делают все


# старт
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    print(message)
    await message.answer(
        "Пожалуйста авторизуйтесь. \n"
        "Для авторизации нажмите Предоставить номер телефона",
        reply_markup=send_phone_number()
    )
    await state.set_state(RegistrationOrLoginStates.send_phone)


@router.message(RegistrationOrLoginStates.send_phone, F.contact)
async def send_phone_for_login(message: Message, state: FSMContext):
    # result = False
    # data = {}
    if message.contact.user_id == message.from_user.id:
        await message.answer(text='Телефон принят, ищу вас в базе пользователей...')
        result, data = login(message.contact.phone_number)
    else:
        await message.answer(text='Хорошая попытка, но не получилось...')
        return
    if result:
        await message.answer(text=f"Добро пожаловать {data['first_name']} {data['patronymic']} "
                                  f"Ваш табельный номер {data['id']}")
        await message.answer(text='Чтобы продолжить нажмите далее',
                             reply_markup=next_button())
        await state.set_state(RegistrationOrLoginStates.logged_in)
    else:
        await state.update_data(user_phone_registration=message.contact.phone_number)
        await message.answer(text="Хм... Ничего не могу найти, похоже вы новый пользователь \n"
                                  "Пожалуйста введите табельный номер",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationOrLoginStates.input_id_registration)


@router.message(RegistrationOrLoginStates.input_id_registration, F.text.lower())
async def registration_user(message: Message, state: FSMContext):
    # global qweqwe
    result, text = validate_id(message.text)
    if result:
        # регистрация нового пользователя в базе, парсим данный из другого бота, получаем их на вход
        await send_user_id(str(result))
        await message.answer(text='Пожалуйста подождите, пока мы ищем вас в базе')
        await asyncio.sleep(5)
        try:
            with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'r', encoding='utf-8') as file:
                user_data = file.read()
            with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'w') as file:
                file.write("0")
        except Exception as ex:
            print(ex)

        user_data = '1299 BC Милевский Георгий Игоревич +79995682544;+79678664791'
        # qweqwe += 1
        # print(qweqwe)
        # await message.answer(text=str(qweqwe))
        user_phone = await state.get_data()
        # print('Это принт!!!', phone_number)
        result, text = create_user(user_data=user_data, phone_number=user_phone['user_phone_registration'],
                                   telegram_user_id=message.from_user.id)
        if result:
            await message.answer(text=text)
        else:
            await message.answer(text=text)
    else:
        await message.answer(text=text)


@router.message(F.text.lower())
async def answer_yes(message: Message):
    await message.answer(
        'Заглушка',
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    pass


if __name__ == '__main__':
    main()
