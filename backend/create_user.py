from sqlalchemy import insert, Connection, exc, select
from backend.model import users, engine


# по-хорошему, весь текст нужно выносить кодами ошибок, как в api, но я пока этого делать не буду, оставлю на следующие
# версии

def create_user(user_data: dict, telegram_user_id):
    # clean_user_data = {'user_id': int(user_data.pop(0)),
    #                    'user_last_name': user_data.pop(0),
    #                    'user_first_name': user_data.pop(0),
    #                    'user_patronymic': user_data.pop(0),
    #                    'user_phone_number': 0,
    #                    }

    stmt = insert(users).values(id=user_data['user_id'],
                                first_name=user_data['user_first_name'],
                                last_name=user_data['user_last_name'],
                                patronymic=user_data['user_patronymic'],
                                phone_number=user_data['user_phone_number'],
                                telegram_user_id=telegram_user_id)
    try:
        with engine.begin() as conn:  # type: Connection
            conn.execute(statement=stmt)
            conn.commit()
            return True, 'Регистрация успешно завершена'
    except exc.IntegrityError:
        stmt = select(users.c.id, users.c.phone_number).where(users.c.id == user_data['user_id'])
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
        if result is not None and result[0] == user_data['user_id']:
            return False, "Ошибка регистрации, такого не должно было быть, но почему-то у меня в базе \n" \
                          f"Табельный номер {result[0]} принадлежит номеру телефона +{result[1]}, " \
                          f"а вы действительно работник нашей АК. Если эта ошибка, " \
                          f"проверь свой введенный табельный, или нажми кнопку \"/help\", админ уже получил" \
                          f" информацию об этой ошибке"
        stmt = select(users.c.id, users.c.phone_number).where(users.c.phone_number == user_data['user_phone_number'])
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
            if result is not None and result[1] == user_data['user_phone_number']:
                return False, f"Ошибка регистрации\n " \
                              f"Вы уже зарегистрированы, но с табельным {user_data['user_id']}, такого быть " \
                              f"не должно и это какая-то ошибка, админ уже знает о ней и разберется, " \
                              f"как только будет время"


def login(phone_number):
    if phone_number[0] == '+':
        phone_number = int(phone_number[1:])
    else:
        phone_number = int(phone_number)

    stmt = select(users.c.id, users.c.first_name, users.c.patronymic, users.c.last_name, users.c.phone_number).where(
        users.c.phone_number == phone_number)
    with engine.connect() as conn:  # type: Connection
        result = conn.execute(statement=stmt)
        result = result.first()
        if result is not None and result[4] == phone_number:
            result = {
                'id': result[0],
                'first_name': result[1],
                'patronymic': result[2],
                'last_name': result[3],
                'phone_number': result[4],
            }
            return True, result
        else:
            result = {}
            return False, result


def main():
    user_data = {'user_id': 1297,
                 'user_last_name': 'Милевский',
                 'user_first_name': 'Георгий',
                 'user_patronymic': 'Игоревич',
                 'user_phone_number': 79995682544,
                 }
    print(create_user(user_data=user_data, telegram_user_id=4734242))
    # print(login('+79995682544'))


if __name__ == '__main__':
    main()
