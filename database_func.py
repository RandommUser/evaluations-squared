# global
import sqlite3
from sqlite3 import Error


def insert_to_table(connection, table, keys, values):
	"""
	insert into a set table in the data base
	connection is the connection to database
	table is table name
	keys is default key tuple
	values is values to add in tuple format
	"""
	if connection == None:
		print("insert_to_table() connection is NULL")
		pass
	elif type(table) != str:
		print("insert_to_table() table is not string")
		pass
	elif type(keys) != tuple:
		print("insert_to_table() table is not tuple")
		pass
	elif type(keys) != values:
		print("insert_to_table() table is not tuple")
		pass
	
	table_keys = ''
	values_len = ''
	for key in keys:
		if table_keys != '':
			table_keys += ','
			values_len += ','
		table_keys += key
		values_len += '?'
	sql = '''INSERT INTO ''' + table + '''
	VALUES(''' + values_len + ''')'''
	cursor = connection.cursor()
	cursor.execute(sql, values)

# create a new table in the database
def create_table(connection, table):
	try:
		cursor = connection.cursor()
		cursor.execute(table)
		print("Made a new table")
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