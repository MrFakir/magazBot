import asyncio
import os

from telethon import TelegramClient
from secret.token_telegram import api_id, api_hash, pars_bot_id
from Config import BASE_DIR
from secret.token_telegram import windows_session_dir

#
# # т.к. бот будет на линуксе, данная конструкция должна работать, но я пишу на винде, поэтому в комменте
# # session_name = os.path.join(BASE_DIR, 'parsed_id', 'sender.session')
session_name = windows_session_dir
#
#
# async def send_user_id(user_id):
#     # return
#     # with open('bot_status.txt', 'r', encoding='utf-8') as file:
#     #     status = file.read()
#     # print(status)
#     # print(type(status))
#     # if status == 'stopped':
#     #     started_listener()
#     pars_bot_id1 = 'me'
#     async with TelegramClient(session=session_name, api_id=api_id, api_hash=api_hash,
#                               system_version="4.16.30-vxCUSTOM") as client:
#         client.loop.run_until_complete(client.send_message(pars_bot_id1, str(user_id)))
#         print('Отправил типо')
#
#
# def main():
#     send_user_id(1111)
#
#
# # async def main():
# #     await send_user_id(1297)
#
#
# if __name__ == '__main__':
#     # asyncio.run(main())
#     main()


import asyncio

from telethon import TelegramClient, events


async def qweqwe():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        await client.send_message('79995682544', 'Hello, myself!')
        print(await client.download_profile_photo('me'))

        @client.on(events.NewMessage(from_users='79995682544'))
        async def handler(event):
            if event.raw_text.lower() == 'hi':
                await event.reply('Hey!')
            if '7' in event.raw_text.lower():
                print('отработал')
                client.disconnect()

        await client.run_until_disconnected()


async def main():
    await qweqwe()


# Only this line changes, the rest will work anywhere.
# Jupyter
# await main()

# Otherwise
if __name__ == '__main__':
    asyncio.run(main())
