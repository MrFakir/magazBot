import os
import time
import asyncio

from telethon import TelegramClient, events
from secret.token_telegram import api_id, api_hash, pars_bot_id, session_name
from Config import BASE_DIR
from secret.token_telegram import windows_session_dir




async def send_user_id(user_id):
    async with TelegramClient(session=windows_session_dir, api_id=api_id, api_hash=api_hash,
                              system_version="4.16.30-vxCUSTOM") as client:
        await asyncio.sleep(5)
        await client.send_message(pars_bot_id, 'Контакты')

        @client.on(events.NewMessage(from_users=pars_bot_id))
        async def listener_chat(event):
            if 'Выберите действие.' in event.raw_text:
                await event.reply('Контакты')

            if 'Напишите фамилию или табельный для поиска номера телефона' in event.raw_text:
                await client.send_message(pars_bot_id, str(user_id))

            if "Не удалось никого найти, может вы опечатались, напишите еще раз" in event.raw_text:
                await client.send_message(pars_bot_id, str(user_id))

            if '7' in event.raw_text:
                print(event.raw_text, 'это будет вывод!!!')
                with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'w', encoding='utf-8') as file:
                    file.write(event.raw_text)
                client.disconnect()

        await client.run_until_disconnected()


async def main():
    await send_user_id(11)


if __name__ == '__main__':
    asyncio.run(main())
