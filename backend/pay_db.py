from sqlalchemy import insert, Connection, exc, select
from model import users, engine, pay
from validators import validate_money, validate_flight
from pay import dry_pay, final_zp_tax
from datetime import date


def create_flight(flight_number, flight_cash, flight_card, user_id=0, flight_date=date.today()):
    if user_id == 0:
        return 'Пожалуйста авторизуйтесь'
    result, message = validate_flight(flight_number)
    if result:
        flight_number = flight_number
    else:
        return message

    result, message = validate_money(flight_cash)
    if result:
        flight_cash = result
    else:
        return message

    result, message = validate_money(flight_card)
    if result:
        flight_card = result
    else:
        return message

    print(type(flight_cash), 'кэш')
    print(type(flight_card), 'карта')

    flight_pay, text = dry_pay(cash=flight_cash, card=flight_card)
    flight_pay = final_zp_tax(flight_pay)

    stmt = insert(pay).values(flight_number=flight_number, flight_date=flight_date, flight_cash=flight_cash,
                              flight_card=flight_card,
                              flight_pay=flight_pay, user_id=user_id, )
    with engine.begin() as conn:  # type: Connection
        conn.execute(statement=stmt)
        conn.commit()
        return 'Рейс успешно добавлен'


def main():
    print(create_flight(flight_number='4234', flight_date=date.today(), flight_cash='25411114', flight_card='2545',
                        user_id=1330))


if __name__ == '__main__':
    main()
