import os
# from pathlib import Path
from Config import BASE_DIR
import sqlalchemy as db

# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR, 123)
# print(BASE_DIR, 321)
# engine = db.create_engine('sqlite:///crew_database.db', echo=True)

# print(os.path.join(BASE_DIR, 'backend', 'crew_database.db'))
engine = db.create_engine(f"sqlite:///{os.path.join(BASE_DIR, 'backend', 'crew_database.db')}")
# engine = db.create_engine('sqlite:///crew_database.db')
connection = engine.connect()
metadate_obj = db.MetaData()

users = db.Table('users', metadate_obj,
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('first_name', db.String),
                 db.Column('last_name', db.String),
                 db.Column('patronymic', db.String),
                 db.Column('phone_number', db.Integer, unique=True),
                 db.Column('telegram_user_id', db.Integer, default=0),
                 )
pay = db.Table('pay', metadate_obj,
               db.Column('id', db.Integer, primary_key=True),
               db.Column('flight_date', db.DATE),
               db.Column('flight_number', db.Integer),
               db.Column('flight_cash', db.Integer),
               db.Column('flight_card', db.Integer),
               db.Column('flight_pay', db.Float),
               db.Column('user_id', db.ForeignKey('users.id'), nullable=False)
               )


def main():
    # print(pay.columns)
    # print()
    metadate_obj.create_all(engine)


if __name__ == '__main__':
    main()
