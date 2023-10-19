import asyncio
import logging
from aiogram import Dispatcher, types, html, F, Bot
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from secret.token_telegram import token

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
# bot = Bot(token="12345678:AaBbCcDdEeFfGgHh")
# Диспетчер
dp = Dispatcher()

bot = Bot(token=token, parse_mode="HTML")


# # Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/special_buttons"),
            types.KeyboardButton(text="/reply_builder"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите меню"
    )
    await message.answer("Выберите меню", reply_markup=keyboard)


@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


@dp.message(F.text.lower())
async def without_puree(message: types.Message):
    print(message.text)


@dp.message(F.contact)
async def test_phone_user(message: types.Message):
    print(message.contact.phone_number)
    if message.contact.user_id == message.from_user.id:
        print(message.contact.phone_number)
    else:
        print('Хорошая попытка, но не получилось...')
    await message.answer('i know u')


@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить контакт", request_contact=True),
    )

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command("name"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, <b>{html.bold(html.quote(command.args))}</b>")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
