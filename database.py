import sqlite3
from sqlite3 import Error

# connect to a SQLite database
def create_connection(db):
	connection = None
	try:
		connection = sqlite3.connect(db)
		print(sqlite3.version)
	except Error as err:
		print(err)
	finally:
		if connection:
			connection.close()