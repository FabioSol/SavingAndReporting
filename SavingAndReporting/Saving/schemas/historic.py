from peewee import *
from SavingAndReporting import database_path

db = SqliteDatabase(database_path, timeout=10)


class Historic(Model):
    datetime = DateTimeField()

    equity_open = FloatField()
    equity_high = FloatField()
    equity_low = FloatField()
    equity_close = FloatField()

    balance_open = FloatField()
    balance_high = FloatField()
    balance_low = FloatField()
    balance_close = FloatField()

    class Meta:
        database = db
