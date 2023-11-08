import os
import asyncio

from telethon import TelegramClient, events
from secret.token_telegram import api_id, api_hash, pars_bot_id, session_name
from Config import BASE_DIR
from secret.token_telegram import windows_session_dir


async def send_user_id(user_id, telegram_user_id):
    print("{:*^100}".format(" Запуск бота для получения ID из базы "))
    async with TelegramClient(session=windows_session_dir, api_id=api_id, api_hash=api_hash,
                              system_version="4.16.30-vxCUSTOM") as client:
        # получилось довольно топорно, но как вышло это единственный работающий вариант
        await asyncio.sleep(5)
        await client.send_message(pars_bot_id, 'Контакты')
        await asyncio.sleep(5)
        await client.send_message(pars_bot_id, str(user_id))

        @client.on(events.NewMessage(from_users=pars_bot_id))
        async def listener_chat(event):
            if "Не удалось никого найти, может вы опечатались, напишите еще раз" in event.raw_text:
                print('Я во внешнем условии проверки: Не удалось никого найти')
                await asyncio.sleep(2)
                print(event.raw_text, 'это будет вывод с ошибкой!')
                with open(os.path.join(BASE_DIR, 'data', str(telegram_user_id)+'.txt'), 'w', encoding='utf-8') as file:
                    file.write('404')
                print("{:*^100}".format(" Бот для получения ID из базы закрыт "))
                client.disconnect()

            if '7' in event.raw_text:
                print('Я во внешнем условии проверки: 7')
                await asyncio.sleep(2)
                print(event.raw_text, 'это будет вывод!!!')
                with open(os.path.join(BASE_DIR, 'data', str(telegram_user_id)+'.txt'), 'w', encoding='utf-8') as file:
                    file.write(event.raw_text)
                print("{:*^100}".format(" Бот для получения ID из базы закрыт "))
                client.disconnect()

        await client.run_until_disconnected()


async def main():
    await send_user_id(11, 6468321)


if __name__ == '__main__':
    asyncio.run(main())
