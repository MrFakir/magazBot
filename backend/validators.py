def validate_name(name, colum):
    if len(name) <= 30:
        return name, ''
    else:
        return False, f'Введите только {colum}'


def validate_flight(flight):
    try:
        flight = int(flight)
        if 99 < flight <= 999999:
            return True, flight
        else:
            return False, 'Введите корректный номер рейса'
    except ValueError:
        return False, 'Введите номер рейса без U6'


def validate_id(user_id):
    try:
        user_id = int(user_id)
        if user_id <= 999999:
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


def main():
    print(validate_name('Георгий', 'Имя'))
    print(validate_flight('123'))


if __name__ == '__main__':
    main()

    # db.Column('first_name', db.String),
    # db.Column('last_name', db.String),
    # db.Column('patronymic', db.String),
    # db.Column('phone_number', db.Integer, unique=True),
