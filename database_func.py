# global
import sqlite3
from sqlite3 import Error


def	select_from_table(connection, table, keys, where = None, values = None, between = 'AND'):
	"""
	select columns from a table
	connection is the connection to database
	table is table name
	keys is tuple, table columns to print
	where is tuple, table keys and the operand e.g. 'key ='
	values is tuple, the values to match
	between is string, the logic for multiple values
	"""
	if connection == None:
		print("select_from_table() connection is NULL")
		return 
	elif type(table) != str:
		print("select_from_table() table is not string")
		print(type(keys))
		return 
	elif type(keys) != tuple:
		print("select_from_table() keys is not tuple")
		print(type(keys))
		return 	
	elif where != None and type(where) != tuple:
		print("select_from_table() 'where' is not tuple")
		print(type(keys))
		return 	
	elif values != None and type(values) != tuple:
		print("select_from_table() values is not tuple")
		print(type(keys))
		return 	
	cursor = connection.cursor()
	select = ''
	for key in keys:
		if select != '':
			select += ","
		select += key
	sql = ''' SELECT ''' + select + ''' FROM ''' + table
	if where != None and values != None and len(where) == len(values): # might cause issues with BETWEEN x AND y
		sql += ''' WHERE'''
		print("lenghts")
		print(len(where))
		print(len(values))
	# parse the matching
		for i in range(len(where)):
			sql += ''' ''' + where[i] + ' ?'
			if i + 1 < len(where): # add the 'between' rule
				sql += ' ' + between
		sql += ';'
		print(sql)
		cursor.execute(sql, values)
	elif where != None and values != None:
		print("Mismatch of where len and values len")
		print(len(where))
		print(len(values))
		return 
	else:
		sql += ';'
		print(sql)
		cursor.execute(sql)
	rows = cursor.fetchall()
	for row in rows:
		print(row)
	return rows

def	select_all_table(connection, table, keys):
	"""
	select columns from a table
	connection is the connection to database
	table is table name
	keys is the rows to print out
	"""
	if connection == None:
		print("select_all_table() connection is NULL")
		return 
	elif type(table) != str:
		print("select_all_table() table is not string")
		return 
	elif type(keys) != tuple:
		print("select_all_table() keys is not tuple")
		print(type(keys))
		return 	
	select = ''
	for key in keys:
		if select != '':
			select += ","
		select += key
	sql = ''' SELECT ''' + select + ''' FROM ''' + table + ''';'''
	print(sql)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	for row in rows:
		print(row)
	return rows
	

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
		return
	elif type(table) != str:
		print("insert_to_table() table is not string")
		return
	elif type(keys) != tuple:
		print("insert_to_table() keys is not tuple")
		return
	elif type(values) != tuple:
		print("insert_to_table() table is not tuple")
		return
	
	table_keys = ''
	values_len = ''
	for key in keys:
		if table_keys != '':
			table_keys += ','
			values_len += ','
		table_keys += key
		values_len += '?'
	sql = ''' INSERT INTO ''' + table + '''
	VALUES(''' + values_len + ''') '''
	print(sql)
	cursor = connection.cursor()
	cursor.execute(sql, values)
	connection.commit()
	return cursor.lastrowid

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