from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.keyboards.for_registration import get_registration_kb, send_phone_number

from backend.validators import validate_id

router = Router()


class RegistrationOrLoginStates(StatesGroup):
    input_phone_registration = State()
    input_id_registration = State()
    input_id_login = State()


@router.message(Command('start'))
async def cmd_start(message: Message):
    print(message)
    await message.answer(
        'Пожалуйста авторизуйтесь. \n'
        f'Новый пользователь? Привет <b>{html.quote(message.chat.username)}</b>! \n '
        f'Пожалуйста пройдите процедуру регистрации, чтобы я мог всё сохранить для вас :)',
        reply_markup=get_registration_kb()
    )


@router.message(F.text.lower() == 'зарегистрироваться')
async def answer_no(message: Message, state: FSMContext):
    await message.answer(
        'Для регистрации в базе, нажмите на кнопку "Предоставить номер телефона"',
        reply_markup=send_phone_number()
    )
    await state.set_state(RegistrationOrLoginStates.input_phone_registration)


@router.message(F.text.lower() == 'войти')
async def answer_no(message: Message, state: FSMContext):
    await message.answer(
        'Пожалуйста введите свой табельный номер для логина',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationOrLoginStates.input_id_login)


@router.message(RegistrationOrLoginStates.input_phone_registration, F.contact)
async def read_id(message: Message, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        await state.update_data(user_phone=message.contact.phone_number)
    else:
        await message.answer(text='Хорошая попытка, но не получилось...')

    await message.answer(
        text='Спасибо. Теперь, пожалуйста, введите свой табельный номер',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationOrLoginStates.input_id_registration)


@router.message(RegistrationOrLoginStates.input_id_registration, F.text.lower())
async def read_id(message: Message, state: FSMContext):
    result, text = validate_id(message.text.lower())
    user_data = await state.get_data()
    if result:
        await message.answer(
            text=f'Спасибо, вы ввели табельный номер {message.text.lower()}, телефон {user_data["user_phone"]} '
                 f'сейчас попробую найти вас в базе АК',
            # Парсер бота с id будет позже Telethon
        )

    else:
        await message.answer(text=text)


@router.message(RegistrationOrLoginStates.input_id_login, F.text.lower())
async def read_id(message: Message, state: FSMContext):
    await message.answer(
        text=f'Спасибо, вы ввели табельный номер {message.text.lower()} сейчас попробую залогиниться',
        # Парсер бота с id будет позже
        # reply_markup=make_row_keyboard(available_food_sizes)
    )
    # await state.set_state(OrderFood.choosing_food_size)


@router.message(F.text.lower())
async def answer_yes(message: Message):
    await message.answer(
        'Заглушка',
        reply_markup=ReplyKeyboardRemove()
    )
