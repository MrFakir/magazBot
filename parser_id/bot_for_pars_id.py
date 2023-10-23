from telethon import TelegramClient
from secret.token_telegram import api_id, api_hash

# Use your own values from my.telegram.org
api_id = api_id
api_hash = api_hash

session_name = '79678664791'

# client = TelegramClient(session, api_id, api_hash)
# client.start()
# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient(session=session_name, api_id=api_id, api_hash=api_hash,
                    system_version="4.16.30-vxCUSTOM") as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!jkhbhbjhb'))

# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
