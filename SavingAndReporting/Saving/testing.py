from SavingAndReporting.Saving.controllers.historic_controller import HistoricController
from peewee import SqliteDatabase
from peewee import *
from datetime import datetime, timedelta
from SavingAndReporting import database_path

# Get the current datetime
current_datetime = datetime.now()

# Calculate yesterday's datetime
yesterday_datetime = current_datetime - timedelta(days=1)

db= SqliteDatabase(database_path)

tables = db.get_tables()

# Print the table names
for table in tables:
    print(table)

rows=HistoricController.get_last_24hrs_historic_rows("192025769")

for row in rows:
    print(row)