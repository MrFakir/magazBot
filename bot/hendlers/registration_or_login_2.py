import asyncio
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from Config import BASE_DIR
from backend.create_user import login, create_user
from backend.validators import validate_id, get_clean_user_data
from bot.keyboards.for_registration import send_phone_number, next_button
from parser_id.bot_for_pars_id import send_user_id

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


async def check_result_file(user_id, user_phone):
    while True:
        print("Внутри цикла проверки файла")
        await asyncio.sleep(3)
        try:
            with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'r', encoding='utf-8') as file:
                user_data = file.read()
                print(user_data)
            if user_data == "0":
                continue
            with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'w', encoding='utf-8') as file:
                file.write("0")
            if user_data == '404':
                message = "Хм... Я не нашёл ничего в базе по этому табельному, попробуйте ввести другой"
                return False, message
            if '7' in user_data:
                result, data = get_clean_user_data(user_id, user_phone)
                return result, data
        except Exception as ex:
            print(ex)


@router.message(RegistrationOrLoginStates.input_id_registration, F.text.lower())
async def registration_user(message: Message, state: FSMContext):
    user_phone = await state.get_data()
    result, text = validate_id(message.text)
    if result:
        # регистрация нового пользователя в базе, парсим данный из другого бота, получаем их на вход
        await send_user_id(str(result))
        await message.answer(text='Пожалуйста подождите, пока мы ищем вас в базе')
        result_check, text_check = await check_result_file(user_id=str(result),
                                                           user_phone=user_phone['user_phone_registration'])
        print("Далее после цикла проверки файла")
        if not result_check:
            await message.answer(text=text_check)
            return
        # await message.answer(text='Проверка файла завершена')
        # await asyncio.sleep(15)

        # заглушка чтото пошло не так, можно попросить по новой ввести тн или закрутить функцию в рекурсию, на пару
        # раз, но я бы лучше попросил ввести по новой, так безопаснее
        # user_data = '1299 BC Милевский Георгий Игоревич +79995682544;+79678664791'
        # qweqwe += 1
        # print(qweqwe)
        # await message.answer(text=str(qweqwe))

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
