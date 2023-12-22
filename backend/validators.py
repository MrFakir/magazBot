import json
import os
from datetime import datetime

from Config import BASE_DIR


def validate_name(name, colum):
    if len(name) <= 30:
        return name, ''
    else:
        return False, f'Введите только {colum}'


def validate_undefined_flight(flight):
    try:
        flight = int(flight)
        if 99 < flight <= 999999:
            return True, flight
        else:
            return False, 'Введите корректный номер рейса, не бывает таких длинных номеров'
    except ValueError:
        return False, 'Введите номер рейса без U6'


def validate_id(user_id):
    try:
        user_id = int(user_id)
        if 999 < user_id <= 999999:
            return user_id, ''
        else:
            return False, 'Табельный номер слишком длинный'
    except ValueError:
        return False, 'Табельный номер должен содержать только цифры'


def validate_money(money):
    try:
        money = int(money)
        if money <= 99999:
            return money, ''
        else:
            return False, 'При всём уважении, проверьте цифру'
    except ValueError:
        return False, 'Введите цифры без копеек'


def get_clean_user_data(user_id_for_check, phone_number, telegram_user_id):
    with open(os.path.join(BASE_DIR, 'data', str(telegram_user_id) + '.txt'), 'r', encoding='utf-8') as file:
        lines = file.readlines()
        print(lines)
        for i in lines:
            if f'{user_id_for_check} ' in i:
                result = i
                break
    user_data = result.replace(';', " ").replace('+', '').split()

    if user_data[1] == 'PU' or user_data[1] == 'BC' or user_data[1] == 'FA':
        user_data.pop(1)
    else:
        return False, "Так так так... кто тут у нас? Бот только для бортпроводников, чужим тут не место :) \n " \
                      "А если это ошибка, админ уже о ней знает, поправит и напишет в телегу =)" \
                      "Ну или проверьте табельный"
    # не очень элегантное решение, переделаю потом, наверное...
    clean_user_data = {'user_id': int(user_data.pop(0)),
                       'user_last_name': user_data.pop(0),
                       'user_first_name': user_data.pop(0),
                       'user_patronymic': user_data.pop(0),
                       'user_phone_number': 0,
                       }

    for i in user_data:
        print(i)
        print('Тип сравниваемого значения', type(i))
        print('Мой номер телефона, который я предоставил', phone_number)
        if i == str(phone_number):
            clean_user_data['user_phone_number'] = int(i)
            break
    print(f'Вывод номера который был записан в клин-дата {clean_user_data["user_phone_number"]}')
    if clean_user_data['user_phone_number'] == 0:
        return False, "Регистрация прервана, предоставленный номер телефона не соответствует введенному табельному"
    return True, clean_user_data


def validate_date(date: str):
    try:
        date = datetime.strptime(date, '%d.%m.%y').date()
        print(type(date))
        return True, date
    except Exception as ex:
        print(ex)
        return False, 'Введите дату UTC в формате ДД.ММ.ГГ, например 20.10.23'


def validate_flight(flight_number):
    try:
        flight_number = int(flight_number)
        # не самое красивое решение, потом как-нибудь лучше сделаю, просто пользователя не хочу просить вводить букву
        # и рейсы некоторые начинаются с 6рки, а в обиходе у нас принято говорить только цифры, без "U6"
        flight_number = f'U6{str(flight_number)}'
        # print(type(flight_number))
    except ValueError:
        # print('Неправильный тип, введите число')
        return False, "Введите номер рейса без U6, только цифры"

    with open(os.path.join(BASE_DIR, 'data', 'clen_button_list.json'), 'r') as file:
        clen_button_list = json.load(file)
    for i in clen_button_list:
        # print(type(i['number']))
        if i['number'] == flight_number:
            return True, i
    else:
        return False, "Хм... Я не нашёл такого рейса, проверьте номер рейса"
        # логику новых рейсов сделаю за пределами валидатора


def main():
    print(validate_name('Георгий', 'Имя'))
    print(validate_flight('123'))


if __name__ == '__main__':
    main()

    # db.Column('first_name', db.String),
    # db.Column('last_name', db.String),
    # db.Column('patronymic', db.String),
    # db.Column('phone_number', db.Integer, unique=True),
