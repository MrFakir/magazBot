from sqlalchemy import insert, Connection, exc, select
from model import users, engine
from validators import validate_name, validate_id


def create_user(user_id, first_name, last_name, patronymic, phone_number):
    result, message = validate_id(user_id=user_id)
    if result:
        user_id = result
    else:
        return message

    result, message = validate_name(name=first_name, colum='')
    if result:
        first_name = result
    else:
        return message
    result, message = validate_name(name=last_name, colum='')
    if result:
        last_name = result
    else:
        return message
    result, message = validate_name(name=patronymic, colum='')
    if result:
        patronymic = result
    else:
        return message

    stmt = insert(users).values(id=user_id, first_name=first_name, last_name=last_name, patronymic=patronymic,
                                phone_number=phone_number)
    try:
        with engine.begin() as conn:  # type: Connection
            conn.execute(statement=stmt)
            conn.commit()
            return 'Регистрация успешно завершена'
    except exc.IntegrityError:
        stmt = select(users.c.id, users.c.phone_number).where(users.c.id == user_id)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
        if result is not None and result[0] == user_id:
            return 'Ошибка регистрации\n' \
                   f'Табельный номер {result[0]} принадлежит номеру телефона +{result[1]}, если эта ошибка, ' \
                   f'проверь свой введенный табельный, или нажми кнопку "Помощь"'
        stmt = select(users.c.id, users.c.phone_number).where(users.c.phone_number == phone_number)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
            if result is not None and result[1] == phone_number:
                return 'Ошибка регистрации\n' \
                       'Вы уже зарегистрированы, чтобы удалить аккаунт нажми кнопку "Помощь"'


def main():
    print(create_user(1331, 'Вася', 'Петров', 'Петрович', 79995682261))


if __name__ == '__main__':
    main()
