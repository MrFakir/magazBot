from telethon import TelegramClient
from secret.token_telegram import api_id, api_hash, pars_bot_id

session_name = 'sender'


def send_user_id(user_id):
    # with open('bot_status.txt', 'r', encoding='utf-8') as file:
    #     status = file.read()
    # print(status)
    # print(type(status))
    # if status == 'stopped':
    #     started_listener()
    with TelegramClient(session=session_name, api_id=api_id, api_hash=api_hash,
                        system_version="4.16.30-vxCUSTOM") as client:
        client.loop.run_until_complete(client.send_message(pars_bot_id, str(user_id)))


def main():
    send_user_id(1297)


if __name__ == '__main__':
    main()
