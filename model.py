# import sqlite3
import sqlalchemy as db

engine = db.create_engine('sqlite:///crew_database.db')
connection = engine.connect()
metadate = db.MetaData()

users = db.Table('users', metadate,
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('first_name', db.Text),
                 db.Column('last_name', db.Text),
                 db.Column('patronymic', db.Text),
                 db.Column('phone_number', db.Integer),
                 )
pay = db.Table('pay', metadate,
               db.Column('id', db.Integer, primary_key=True),
               db.Column('flight_number', db.Text),
               db.Column('flight_pay', db.Float),
               db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
               )



metadate.create_all(engine)
