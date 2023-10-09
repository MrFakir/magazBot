from sqlalchemy import insert, Connection, exc, select
from model import users, engine


# from sqlite3 import IntegrityError


def create_user(id, first_name, last_name, patronymic, phone_number):
    stmt = insert(users).values(id=id, first_name=first_name, last_name=last_name, patronymic=patronymic,
                                phone_number=phone_number)
    # print(stmt)
    try:
        with engine.begin() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            conn.commit()
    except exc.IntegrityError:
        # print('Ошибка ключа')
        # stmt = select(users)
        # print(stmt)
        stmt = select(users.c.id, users.c.phone_number).where(users.c.id == id)
        # print(stmt)
        with engine.connect() as conn:  # type: Connection
            result = conn.execute(statement=stmt)
            # print()
            row = result.first()
            # for row in result:
            #     print(row)
        print(
            f'Табельный номер {row[0]} принадлежит номеру телефона +{row[1]}, если эта ошибка, '
            f'проверь свой введенный табельный, или нажми кнопку "Помощь"')


def main():
    create_user(1325, 'Вася', 'Петров', 'Петрович', 79995682244)


if main() == '__name__':
    main()
