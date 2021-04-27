#!/bin/python3
# global
import sys
# local
import database, helpers, database_func, api42

# Basic commands
"""
	# print students table for the campus
	students = database_func.select_from_table(connection, "students", database.keys['students'], (("campus_id =",)), (("13",)))
	helpers.print_db(students, database.keys['students'])
	# print the projects and their average times
	projects = database_func.select_from_table(connection, "projects", (("name", "average_time")), (("campus_id =",)), ((database.setup['campus'],)))
	helpers.print_db(projects, (("name", "average_time")), False)

# print student table
students = database_func.select_from_table(connection, "students", database.keys["students"], (("campus_id",)), ((database.setup['campus'],)))
helpers.print_db(students, database.keys["students"])

# projects and their average eval time
projects = database_func.select_from_table(connection, "projects", (("name", "average_time")), (("campus_id",)), ((database.setup['campus'],)))
helpers.print_db(students, (("name", "average_time")), False)

"""

def main():
	try:
	token = api42.get_token()
	connection = database.establish()
	database.setup_db(connection, token)
	except:
		print("Error")
	finally:
		if connection != None:
			connection.close()
		exit()

if __name__ == '__main__':
	main()