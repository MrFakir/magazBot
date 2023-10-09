# import sqlite3
import sqlalchemy as db

# engine = db.create_engine('sqlite:///crew_database.db', echo=True)
engine = db.create_engine('sqlite:///crew_database.db')
connection = engine.connect()
metadate_obj = db.MetaData()

users = db.Table('users', metadate_obj,
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('first_name', db.String),
                 db.Column('last_name', db.String),
                 db.Column('patronymic', db.String),
                 db.Column('phone_number', db.Integer, unique=True),
                 )
pay = db.Table('pay', metadate_obj,
               db.Column('id', db.Integer, primary_key=True),
               db.Column('flight_number', db.Integer),
               db.Column('flight_pay', db.Float),
               db.Column('user_id', db.ForeignKey('users.id'), nullable=False)
               )


def main():
    # print(pay.columns)
    # print()
    metadate_obj.create_all(engine)


if __name__ == '__main__':
    main()


