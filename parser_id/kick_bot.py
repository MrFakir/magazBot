# import os
# import time
#
#
# def main():
#     while True:
#         time.sleep(2)
#         with open('bot_status.txt', 'r', encoding='utf-8') as file:
#             status = file.read()
#         print(status)
#         print(type(status))
#         if status == 'stopped':
#             os.system("start cmd /k python bot_for_pars_id_listener.py")
#
#
# if __name__ == '__main__':
#     main()
