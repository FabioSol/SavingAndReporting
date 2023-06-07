import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the database file
relative_path = 'Saving/db/accounts.db'

# Create the absolute path by joining the current directory and the relative path
database_path = os.path.join(current_dir, relative_path)