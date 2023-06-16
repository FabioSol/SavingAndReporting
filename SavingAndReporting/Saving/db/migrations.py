from peewee import SqliteDatabase
from SavingAndReporting.Saving.schemas.account import Account
from SavingAndReporting.Saving.controllers.account_controller import AccountController
from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
from datetime import datetime
from SavingAndReporting import database_path
import os
import csv


def migrate():
    def create_db(path: str) -> bool:
        if not os.path.isfile(path):
            db = SqliteDatabase(path)
            db.create_tables([Account])
            return True

    def process_csv_files(directory, account):
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                open_csv(file_path, account)

    def open_csv(file_path, account):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            past_equity_open = None
            past_equity_high = None
            past_equity_low = None
            past_equity_close = None
            first = True
            for row in reader:
                # Process each row
                if row[1] != 'Open':
                    time = datetime.strptime(row[0][-19:], "%Y.%m.%d %H:%M:%S")
                    equity_open = float(row[1])
                    equity_high = float(row[2])
                    equity_low = float(row[3])
                    equity_close = float(row[4])

                    if (past_equity_open == equity_open) & (past_equity_high == equity_high) & (
                            past_equity_low == equity_low) & (past_equity_close == equity_close):
                        balance_open = equity_open
                        balance_high = equity_high
                        balance_low = equity_low
                        balance_close = equity_close

                    elif first:
                        balance_open = equity_open
                        balance_high = equity_high
                        balance_low = equity_low
                        balance_close = equity_close
                        first = False

                    else:
                        balance_open = past_balance_open
                        balance_high = past_balance_high
                        balance_low = past_balance_low
                        balance_close = past_balance_close

                    HistoricController.add_historic_row(account=account,
                                                        date_time=time,
                                                        equity_open=equity_open,
                                                        equity_high=equity_high,
                                                        equity_low=equity_low,
                                                        equity_close=equity_close,
                                                        balance_open=balance_open,
                                                        balance_high=balance_high,
                                                        balance_low=balance_low,
                                                        balance_close=balance_close)

                    past_equity_open = equity_open
                    past_equity_high = equity_high
                    past_equity_low = equity_low
                    past_equity_close = equity_close

                    past_balance_open = balance_open
                    past_balance_high = balance_high
                    past_balance_low = balance_low
                    past_balance_close = balance_close

    if create_db(database_path):

        account_ids = ["15843602", "15843603", "15843604", "15843606", "15843607", "192025769"]
        initial_amounts = [10_000, 10_000, 10_000, 10_000, 10_000, 2_112]
        account_types = ["CentDemo(USC)", "CentDemo(USC)", "CentDemo(USC)", "CentDemo(USC)", "CentDemo(USC)", "CentReal(USC)"]

        test_data_path = "test_data/"

        for id, am, ty in zip(account_ids, initial_amounts, account_types):
            account = AccountController.create_account(account_id=id, initial_amount=am, type_of_account=ty)
            path = test_data_path + id
            process_csv_files(path, account)

    else:
        print("previously made")


