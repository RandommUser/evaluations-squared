# global
import sqlite3
from sqlite3 import Error

student_table = """CREATE TABLE IF NOT EXISTS students (
	id integer PRIMARY KEY,
	user_id integer NOT NULL,
	login text NOT NULL,
	url text NOT NULL
);"""

# create a new table in the database
def create_table(connection, table):
	try:
		cursor = connection.cursor()
		cursor.execute(table)
	except Error as err:
		print(err)

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
			#connection.close()
			return connection