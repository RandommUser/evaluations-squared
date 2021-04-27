# global
import sqlite3
from sqlite3 import Error

# Calculate project eval time average. Does not get it right
def	project_average(connection, campus, proj_table = "projects", eval_table = "evaluations"):
	if connection == None:
		raise TypeError("select_distinct() connection is NULL")
		return
	campus = str(campus)
	# unique projects
	projects = select_from_table(connection, proj_table, (("project_id",)), (("campus_id =",)), (("13",)))
	for project in projects:
		amount = 0
		i = 0
		# array of all eval times for project
		time_taken = select_from_table(connection, eval_table, (("time_start", "time_end")), (("campus_id =", "project_id =")), (("13", project[0])))
		for single in time_taken:
			amount += single[0] - single[1]
			i += 1
		amount = float(amount / i / 60)
		update_table(connection, "projects", (("average_time",)), ((amount,)), (("campus_id =", "project_id =")), (("13", project[0])))

# find unique rows
def select_distinct(connection, table, keys):
	if connection == None:
		raise TypeError("select_distinct() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("select_distinct() table is not string")
		print(type(table))
		return 
	elif type(keys) != str:
		raise TypeError("select_distinct() keys is not str")
		print(type(keys))
		return 
	sql = ''' SELECT DISTINCT ''' + keys + ''' FROM ''' + table + ''';'''
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	return rows

# Get student ids of a campus into a string array
def get_students_arr(connection, campus, limit = 50, key = "user_id", where = "campus_id", table = "students"):
	if connection == None:
		raise TypeError("get_students_arr() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("get_students_arr() table is not string")
		print(type(table))
		return 
	elif type(limit) != int:
		raise TypeError("get_students_arr() limit is not int")
		print(type(limit))
		return 
	elif type(key) != str:
		raise TypeError("get_students_arr() key is not str")
		print(type(key))
		return 
	elif type(where) != str:
		raise TypeError("get_students_arr() where is not str")
		print(type(where))
		return 

	ret = []
	sql = ''' SELECT ''' + key + ''' FROM ''' + table + ''' WHERE ''' + where + ''' = ''' + campus + ''';'''
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	i = 0
	student_string = ""
	for row in rows:
		if student_string != "":
			student_string += ","
		student_string += str(row[0])
		i += 1
		if i == limit:
			ret.append(student_string)
			student_string = ""
			i = 0
	return ret

# helper function for "WHERE ... " parts
def where_values(where, values, between):
	ret = ""
	if where != None and values != None and len(where) == len(values): # might cause issues with BETWEEN x AND y
		ret += ''' WHERE'''
	# parse the matching
		for i in range(len(where)):
			ret += ''' ''' + where[i] + ' ?'
			if i + 1 < len(where): # add the 'between' rule
				ret += ' ' + between
		return ret
	elif where != None and values != None:
		print("Mismatch of where len and values len")
		print(len(where))
		print(len(values))
		return ret
	else:
		return ret

# Delete from a table
def delete_where(connection, table, where, values, between = 'AND'):
	if connection == None:
		raise TypeError("delete_where() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("delete_where() table is not string")
		print(type(table))
		return 
	elif type(where) != tuple:
		raise TypeError("delete_where() 'where' is not tuple")
		print(type(where))
		return 	
	elif type(values) != tuple:
		raise TypeError("delete_where() values is not tuple")
		print(type(values))
		return 
	sql = ' DELETE FROM ' + table
	sql += where_values(where, values, between) + ';'
	print(sql)
	cursor = connection.cursor()
	cursor.execute(sql, values)

# Select from table where values match
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
		raise TypeError("select_from_table() connection is NULL")
		return 
	elif type(table) != str:
		raise TypeError("select_from_table() table is not string")
		print(type(table))
		return 
	elif type(keys) != tuple:
		raise TypeError("select_from_table() keys is not tuple")
		print(type(keys))
		return 	
	elif where != None and type(where) != tuple:
		raise TypeError("select_from_table() 'where' is not tuple")
		print(type(where))
		return 	
	elif values != None and type(values) != tuple:
		raise TypeError("select_from_table() values is not tuple")
		print(type(values))
		return 	
	cursor = connection.cursor()
	select = ''
	for key in keys:
		if select != '':
			select += ","
		select += key
	sql = ''' SELECT ''' + select + ''' FROM ''' + table
	sql += where_values(where, values, between) + ';'
	if values != None:
		cursor.execute(sql, values)
	else:
		cursor.execute(sql)
	rows = cursor.fetchall()
	return rows

# Select all rows from a table
def	select_all_table(connection, table, keys):
	"""
	select columns from a table
	connection is the connection to database
	table is table name
	keys is the rows to print out
	"""
	if connection == None:
		raise TypeError("select_all_table() connection is NULL")
		return 
	elif type(table) != str:
		raise TypeError("select_all_table() table is not string")
		return 
	elif type(keys) != tuple:
		raise TypeError("select_all_table() keys is not tuple")
		print(type(keys))
		return 	
	select = 'rowid'
	for key in keys:
		if select != '':
			select += ","
		select += key
	sql = ''' SELECT ''' + select + ''' FROM ''' + table + ''';'''
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	return rows
	
# Insert data to table
def insert_into_table(connection, table, keys, values):
	"""
	insert into a set table in the data base
	connection is the connection to database
	table is table name
	keys is default key tuple
	values is values to add in tuple format
	"""
	if connection == None:
		raise TypeError("insert_to_table() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("insert_to_table() table is not string")
		return
	elif type(keys) != tuple:
		raise TypeError("insert_to_table() keys is not tuple")
		return
	elif type(values) != tuple:
		raise TypeError("insert_to_table() table is not tuple")
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
	return cursor.lastrowid

# Update columns in rows where match
def update_table(connection, table, update_keys, update_values, where, values):
	if connection == None:
		raise TypeError("update_table() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("update_table() table is not string")
		return
	elif type(update_keys) != tuple:
		raise TypeError("update_table() update_keys is not tuple")
		return
	elif type(update_values) != tuple:
		raise TypeError("update_table() update_values is not tuple")
		return
	elif type(where) != tuple:
		raise TypeError("update_table() where is not tuple")
		return
	elif type(values) != tuple:
		raise TypeError("update_table() values is not tuple")
		return
	insert = ""
	for key in update_keys:
		if insert != "":
			insert += ", "
		insert += key + ' = ?'
	sql = ''' UPDATE ''' + table + ''' SET ''' + insert
	sql += where_values(where, values, "AND") + ';'
	#print(sql)
	cursor = connection.cursor()
	cursor.execute(sql, update_values + values)

# Add or delete + add a row
# creates a lot of rowid increases so maybe could do a custom one
def replace_into_table(connection, table, keys, values):
	"""
	insert into a set table in the data base
	connection is the connection to database
	table is table name
	keys is default key tuple
	values is values to add in tuple format
	"""
	if connection == None:
		raise TypeError("insert_to_table() connection is NULL")
		return
	elif type(table) != str:
		raise TypeError("insert_to_table() table is not string")
		return
	elif type(keys) != tuple:
		raise TypeError("insert_to_table() keys is not tuple")
		return
	elif type(values) != tuple:
		raise TypeError("insert_to_table() table is not tuple")
		return
	
	table_keys = ''
	values_len = ''
	for key in keys:
		if table_keys != '':
			table_keys += ','
			values_len += ','
		table_keys += key
		values_len += '?'
	sql = ''' REPLACE INTO ''' + table + '''
	VALUES(''' + values_len + ''') '''
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
	except Error as err:
		print(err)
	finally:
		if connection:
			return connection

if __name__ == '__main__':
	exit()
