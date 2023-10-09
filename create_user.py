from sqlalchemy import insert, Connection, exc, select
from model import users, engine


def create_user(user_id, first_name, last_name, patronymic, phone_number):
    stmt = insert(users).values(id=user_id, first_name=first_name, last_name=last_name, patronymic=patronymic,
                                phone_number=phone_number)
    try:
        with engine.begin() as conn:  # type: Connection
            conn.execute(statement=stmt)
            conn.commit()
            print('Регистрация успешно завершена')
    except exc.IntegrityError:
        print('Ошибка регистрации')
        stmt = select(users.c.id, users.c.phone_number).where(users.c.id == user_id)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
        if result is not None and result[0] == user_id:
            print(
                f'Табельный номер {result[0]} принадлежит номеру телефона +{result[1]}, если эта ошибка, '
                f'проверь свой введенный табельный, или нажми кнопку "Помощь"')
            return
        stmt = select(users.c.id, users.c.phone_number).where(users.c.phone_number == phone_number)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            result = result.first()
            if result is not None and result[1] == phone_number:
                print('Вы уже зарегистрированы, чтобы удалить аккаунт нажми кнопку "Помощь"')
            return


def main():
    create_user(1331, 'Васярпоагирнвоодинрчтровнртровчивтрййййййю', 'Петров', 'Петрович', 79995682261)


if __name__ == '__main__':
    main()
