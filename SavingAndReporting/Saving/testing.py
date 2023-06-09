from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
from SavingAndReporting.Saving.controllers.account_controller import AccountController
from peewee import SqliteDatabase
from peewee import *
from datetime import datetime, timedelta
from SavingAndReporting import database_path
from schemas.account import Account
# Get the current datetime
current_datetime = datetime.now()

# Calculate yesterday's datetime
yesterday_datetime = current_datetime - timedelta(days=1)


#account=AccountController.create_account("1234",1000,"testing")

#db=SqliteDatabase(database_path)
#print(db.get_tables())


#print(AccountController.erase_account("1234"))

#print(db.get_tables())
AccountController.erase_account("123456")