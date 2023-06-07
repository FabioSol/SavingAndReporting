from SavingAndReporting.Saving.schemas.account import Account
from SavingAndReporting.Saving.schemas.historic import Historic
from peewee import *
import datetime

db = SqliteDatabase("./db/accounts.db", timeout=10)


class HistoricController:

    @staticmethod
    def create_historic_table(account: Account):
        global table_name
        table_name = f'historic_{account.account_id}'

        class HistoricTable(Historic):
            class Meta:
                table_name = table_name
                database = db

        HistoricTable.create_table()
        return HistoricTable

    @staticmethod
    def add_historic_row(account: Account, date_time, equity_open, equity_high, equity_low, equity_close,
                         balance_open, balance_high, balance_low, balance_close):
        # Get the historic table for the specified account
        global table_name
        table_name = f'historic_{account.account_id}'

        class HistoricTable(Historic):
            class Meta:
                table_name = table_name

        # Create a new row and save it
        row = HistoricTable(datetime=date_time, equity_open=equity_open, equity_high=equity_high,
                            equity_low=equity_low, equity_close=equity_close, balance_open=balance_open,
                            balance_high=balance_high, balance_low=balance_low, balance_close=balance_close)
        row.save()

    @staticmethod
    def get_all_historic_rows(account_id: str):
        # Get the historic table for the specified account
        global table_name

        table_name = f'historic_{account_id}'

        class HistoricTable(Historic):
            class Meta:
                table_name = table_name

        # Retrieve all rows from the historic table
        rows = HistoricTable.select().execute()
        return list(rows)

    @staticmethod
    def get_historic_rows_since(account_id: str, since_date: datetime):
        # Get the historic table for the specified account
        global table_name

        table_name = f'historic_{account_id}'

        class HistoricTable(Historic):
            class Meta:
                table_name = table_name

        # Retrieve rows from the historic table since the specified date
        rows = HistoricTable.select().where(HistoricTable.datetime >= since_date).execute()
        return list(rows)

    @staticmethod
    def get_last_historic_row(account_id: str):
        # Get the historic table for the specified account
        global table_name
        table_name = f'historic_{account_id}'

        class HistoricTable(Historic):
            class Meta:
                table_name = table_name

        # Retrieve the last row from the historic table
        last_row = HistoricTable.select().order_by(HistoricTable.datetime.desc()).limit(1).execute()
        return last_row.first() if last_row else None
