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
from bot.keyboards.for_registration import send_phone_number, next_button, cry_button
from parser_id.bot_for_pars_id import send_user_id
from secret.token_telegram import author

router = Router()


# список состояний пользователей, лишние уберу позже, а список оставлю здесь,
# только в этом модуле, используются разные состояния, в других только logged_in
class RegistrationOrLoginStates(StatesGroup):
    input_phone_registration = State()
    input_id_registration = State()
    input_phone_login = State()
    input_id_login = State()
    send_phone = State()
    logged_in = State()


# старт
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    print(message)
    await message.answer(
        text="Пожалуйста авторизуйтесь. \n"
             "Для авторизации нажмите Предоставить номер телефона",
        reply_markup=send_phone_number()
    )
    await state.set_state(RegistrationOrLoginStates.send_phone)


@router.message(Command('help'))
async def cmd_start(message: Message):
    print(message)
    await message.answer(
        text="Ваша проблема и все данные с неё были отправлены админу. Если вы хотите что-то добавить, "
             f"пишите админу: {author}",
        reply_markup=send_phone_number()
    )
    # await state.set_state(RegistrationOrLoginStates.send_phone)


# считываем номер телефона из чата
@router.message(RegistrationOrLoginStates.send_phone, F.contact)
async def send_phone_for_login(message: Message, state: FSMContext):
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


# проверка файла с результатами работа парсер-бота, ей тут не место, подумаю куда ёё деть,
# а может вообще убирать буду
async def check_result_file(user_id, user_phone, telegram_user_id):
    while True:
        print("Внутри цикла проверки файла")
        await asyncio.sleep(3)
        try:
            with open(os.path.join(BASE_DIR, 'data', str(telegram_user_id) + '.txt'), 'r', encoding='utf-8') as file:
                user_data = file.read()
                print(user_data)
            if user_data == '404':
                message = "Хм... Я не нашёл ничего в базе по этому табельному, попробуйте ввести другой"
                return False, message
            if '7' in user_data:
                result, data = get_clean_user_data(user_id, user_phone, telegram_user_id=telegram_user_id)
                # хотел удалять файл, после получения результатов, но потом решил, пусть будут,
                # вдруг данные мне пригодятся :)
                return result, data
        except Exception as ex:
            print(ex)
            return False, "При поиске в базе что-то пошло не так, админ уже знает об этом," \
                          "Вы можете попробовать ещё раз прислать свой табельный, вдруг всё заработает :)"


# регистрация
@router.message(RegistrationOrLoginStates.input_id_registration, F.text.lower())
async def registration_user(message: Message, state: FSMContext):
    user_phone = await state.get_data()
    result_valid, valid_data = validate_id(message.text)
    if result_valid:
        # Регистрация нового пользователя в базе, парсим данный из другого бота, получаем их на вход.
        # Здесь нужно организовать очередь, т.к. возможен вариант одновременной регистрации двоих пользователей,
        # а аккаунт для парсинга базы только один, но делать я буду это в последнюю очередь
        await message.answer(text='Пожалуйста подождите, пока мы ищем вас в базе')
        await send_user_id(user_id=str(result_valid), telegram_user_id=message.from_user.id)
        await message.answer(text='Что-то нашли, посмотрим...')
        # проверка результата, на выходе получает чистые данные в виде словаря
        result_check, check_data = await check_result_file(user_id=str(result_valid),
                                                           user_phone=user_phone['user_phone_registration'],
                                                           telegram_user_id=message.from_user.id)
        print("Далее после цикла проверки файла")
        if not result_check:
            await message.answer(text=check_data)
            await message.answer(text="Введите табельный")
            return

        if result_check:
            # если все данные в порядке, регистрируем пользователя
            result_registration, registration_data = create_user(user_data=check_data,
                                                                 telegram_user_id=message.from_user.id)
            if result_registration:
                await message.answer(text=registration_data)
                await message.answer(text="Пожалуйста нажмите кнопку далее, чтобы продолжить работу с ботом",
                                     reply_markup=next_button())
                await state.set_state(RegistrationOrLoginStates.logged_in)

            else:
                await message.answer(text=registration_data, reply_markup=cry_button())
    else:
        await message.answer(text=valid_data)
        await message.answer(text="Введите табельный")


# А это уже отдельный модуль будет
# @router.message(RegistrationOrLoginStates.logged_in, F.text.lower() == 'далее')
# async def main_menu(message: Message):
#     await message.answer(
#         text='Всякий функционал программы',
#         reply_markup=ReplyKeyboardRemove()
#     )


# @router.message(F.text.lower())
# async def mess_stub(message: Message):
#     await message.answer(
#         text='Заглушка',
#         reply_markup=ReplyKeyboardRemove()
#     )


def main():
    pass


if __name__ == '__main__':
    main()
