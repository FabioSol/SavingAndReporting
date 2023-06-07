from peewee import *

db = SqliteDatabase("./db/accounts.db", timeout=10)


class Account(Model):
    account_id = CharField(primary_key=True)
    initial_amount = FloatField()
    type_of_account = CharField()

    class Meta:
        database = db

