import asyncio
import logging
from aiogram import Dispatcher, Bot
from secret.token_telegram import token
from hendlers import registration_or_login


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        registration_or_login.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
