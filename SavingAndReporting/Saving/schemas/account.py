from peewee import *
from SavingAndReporting import database_path

db = SqliteDatabase(database_path, timeout=10)


class Account(Model):
    account_id = CharField(primary_key=True)
    initial_amount = FloatField()
    type_of_account = CharField()

    class Meta:
        database = db

