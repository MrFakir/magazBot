import asyncio
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from Config import BASE_DIR
from backend.create_user import login, create_user
from backend.validators import validate_id, get_clean_user_data
from bot.hendlers.registration_or_login_2 import RegistrationOrLoginStates
from bot.keyboards.for_registration import send_phone_number, next_button, cry_button
from bot.keyboards.for_main_body import main_menu_kb
from parser_id.bot_for_pars_id import send_user_id

router = Router()


# заглушка авторизации, но пока заглушка для всего
@router.message(F.text.lower())
async def main_menu(message: Message):
    await message.answer(
        text='Пожалуйста авторизуйтесь, для авторизации нажмите /start',
    )


def main():
    pass


if __name__ == '__main__':
    main()
