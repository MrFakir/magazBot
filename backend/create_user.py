from sqlalchemy import insert, Connection, exc, select
from backend.model import users, engine
# from backend.validators import validate_name, validate_id


# def create_user(user_id, first_name, last_name, patronymic, phone_number):
#     result, message = validate_id(user_id=user_id)
#     if result:
#         user_id = result
#     else:
#         return message
#
#     result, message = validate_name(name=first_name, colum='')
#     if result:
#         first_name = result
#     else:
#         return message
#     result, message = validate_name(name=last_name, colum='')
#     if result:
#         last_name = result
#     else:
#         return message
#     result, message = validate_name(name=patronymic, colum='')
#     if result:
#         patronymic = result
#     else:
#         return message
#
#     stmt = insert(users).values(id=user_id, first_name=first_name, last_name=last_name, patronymic=patronymic,
#                                 phone_number=phone_number)
#     try:
#         with engine.begin() as conn:  # type: Connection
#             conn.execute(statement=stmt)
#             conn.commit()
#             return 'Регистрация успешно завершена'
#     except exc.IntegrityError:
#         stmt = select(users.c.id, users.c.phone_number).where(users.c.id == user_id)
#         with engine.connect() as conn:  # type: Connection
#             result = conn.execute(statement=stmt)
#             result = result.first()
#         if result is not None and result[0] == user_id:
#             return 'Ошибка регистрации\n' \
#                    f'Табельный номер {result[0]} принадлежит номеру телефона +{result[1]}, если эта ошибка, ' \
#                    f'проверь свой введенный табельный, или нажми кнопку "Помощь"'
#         stmt = select(users.c.id, users.c.phone_number).where(users.c.phone_number == phone_number)
#         with engine.connect() as conn:  # type: Connection
#             result = conn.execute(statement=stmt)
#             result = result.first()
#             if result is not None and result[1] == phone_number:
#                 return 'Ошибка регистрации\n' \
#                        'Вы уже зарегистрированы, чтобы удалить аккаунт нажми кнопку "Помощь"'

# по-хорошему, весь текст нужно выносить кодами ошибок, как в api, но я пока этого делать не буду, оставлю на следующие
# версии

def create_user(user_data, phone_number, telegram_user_id):
    user_data = user_data.replace(';', ' ').replace('+', '').split()
    print(user_data[1], '!!!!!!!!!!!!!!!!!!!!!!!!!')

    if user_data[1] == 'PU' or user_data[1] == 'BC' or user_data[1] == 'FA':
        pass
    else:
        return False, "Так так так... кто тут у нас? Бот только для бортпроводников, чужим тут не место :) \n " \
                      "А если это ошибка, админ уже о ней знает, поправит и напишет в телегу =)" \
                      "Ну или проверьте табельный"
    # не очень элегантное решение, переделаю потом, наверное...
    user_id = int(user_data.pop(0))
    user_data.pop(0)
    user_last_name = user_data.pop(0)
    user_first_name = user_data.pop(0)
    user_patronymic = user_data.pop(0)
    user_phone_number = 0
    for i in user_data:
        if i == phone_number:
            user_phone_number = int(i)
            break
    if user_phone_number == 0:
        return False, "Регистрация прервана, предоставленный номер телефона не соответствует введенному табельному"

    stmt = insert(users).values(id=user_id, first_name=user_first_name, last_name=user_last_name,
                                patronymic=user_patronymic,
                                phone_number=user_phone_number, telegram_user_id=telegram_user_id)
    try:
        with engine.begin() as conn:  # type: Connection
            conn.execute(statement=stmt)
            conn.commit()
            return True, 'Регистрация успешно завершена'
    except exc.IntegrityError:
        stmt = select(users.c.id, users.c.phone_number).where(users.c.id == user_id)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
        if result is not None and result[0] == user_id:
            return False, 'Ошибка регистрации, такого не должно было быть, но почему-то у меня в базе \n' \
                   f'Табельный номер {result[0]} принадлежит номеру телефона +{result[1]}, ' \
                          f'а вы действительно работник нашей АК. Если эта ошибка, ' \
                   f'проверь свой введенный табельный, или нажми кнопку "Помощь", админ уже получил' \
                   f' информацию об этой ошибке'
        stmt = select(users.c.id, users.c.phone_number).where(users.c.phone_number == user_phone_number)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
            if result is not None and result[1] == user_phone_number:
                return False, 'Ошибка регистрации\n' \
                       f'Вы уже зарегистрированы, но с табельным {user_id}, такого быть не должно и это ' \
                       f'какая-то ошибка, админ уже знает о ней и разберется, как только будет время'


def login(phone_number):
    # noinspection PyTypeChecker
    # print(phone_number)
    # print(type(phone_number))
    if phone_number[0] == '+':
        phone_number = int(phone_number[1:])
    else:
        phone_number = int(phone_number)
    # print(phone_number)
    # print(type(phone_number))
    stmt = select(users.c.id, users.c.first_name, users.c.patronymic, users.c.last_name, users.c.phone_number).where(
        users.c.phone_number == phone_number)
    with engine.connect() as conn:  # type: Connection
        result = conn.execute(statement=stmt)
        result = result.first()
        # print(result)
        # print(type(result[4]))
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
    pass
    print(create_user(user_data='1297 BC Милевский Георгий Игоревич +79995682545;+79678664791',
                      phone_number='79995682545', telegram_user_id=4734242))
    # print(login('+79995682544'))


if __name__ == '__main__':
    main()
