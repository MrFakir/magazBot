import os
import time
import asyncio

from telethon import TelegramClient, events
from secret.token_telegram import api_id, api_hash, pars_bot_id, session_name
from Config import BASE_DIR

# запускаем очередь пользователей, когда один начинает работы,
# остальных вешаем в ожидание и раздаем номера, у первого запускаем "старт", когда первый
# финиш, запускаем второго и обновляем список
# api_id = my_api_id
# api_hash = my_api_hash
# session_name = '79678664791'

client = TelegramClient(session=session_name, api_id=api_id, api_hash=api_hash,
                        system_version="4.16.30-vxCUSTOM")


@client.on(events.NewMessage(from_users=pars_bot_id))
async def my_event_handler(event):
    message = event.raw_text.lower()
    print(message)
    if 'Выберите действие.' in event.raw_text:
        await asyncio.sleep(5)
        await event.reply('Контакты')
    if 'Напишите фамилию или табельный для поиска номера телефона' in event.raw_text:
        time.sleep(5)
        print('Бот готов к приему сообщений')
    if 'Не удалось никого найти, может вы опечатались, напишите еще раз' in event.raw_text:
        print('Бот готов к приему сообщений')
    if '7' in event.raw_text:
        print(event.raw_text, 'это будет вывод!!!')
        with open(os.path.join(BASE_DIR, 'data', 'file_user_data.txt'), 'w') as file:
            file.write(event.raw_text)
        await asyncio.sleep(5)
        await event.reply('Контакты')
    # if '7967' in event.raw_text:
    #     a = int(event.raw_text)


def main():
    client.start()
    # если бот запущен, то в переменной окружения висит started, если не запущен, то stopped и мы перед отправкой пинаем
    # бота чтобы он запустился
    # сделаю лучше отдельным скриптом на стороне сервера перезапуск и всё

    print('Бот запущен')
    # with open('bot_status.txt', 'w') as file:
    #     file.write("started")
    # print('В файл или переменную окружения ')
    # try:
    client.run_until_disconnected()
        # client.loop.run_until_complete(my_event_handler)
    # except Exception as err:
    #     print(err)
    #     with open('bot_status.txt', 'w') as file:
    #         file.write("stopped")


if __name__ == '__main__':
    main()
