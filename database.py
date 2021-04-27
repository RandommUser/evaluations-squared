# global
import sqlite3
from sqlite3 import Error
# local
import database_func


# database name
database_name = '42API.db'

# setup default values
# eval_time_range is the time from now - eval_time_range to fetch evaluations from the campus students
setup = {
	"campus" : "Helsinki",
	"eval_time_range" : 60 * 60 * 24 * 365
}

# table key tuples used in insert_to_table()
keys = {
	"campus" : tuple(("campus_id", "name")),
	"students" : tuple(("user_id", "login", "campus_id", "url")),
	"projects" : tuple(("project_id", "name", "campus_id", "average_time")),
	"evaluations" : tuple(("eval_id", "project_id", "scale_id", "time_start", \
		"time_end", "corrected_id", "corrected_feedback", "corrected_rating", \
			"corrector_id", "corrector_feedback", "corrector_mark", "corrector_flag"))
}


# unique value in each table that cannot match with any other entry
unique = {
	"campus" : "campus_id",
	"students" : "user_id"
}

# table structures
campus_table = """CREATE TABLE IF NOT EXISTS campus (
	campus_id integer NOT NULL UNIQUE,
	name text NOT NULL
);"""

students_table = """CREATE TABLE IF NOT EXISTS students (
	user_id integer NOT NULL UNIQUE,
	login text NOT NULL,
	campus_id integer NOT NULL,
	url text NOT NULL
);"""

projects_table = """CREATE TABLE IF NOT EXISTS projects (
	project_id integer NOT NULL,
	name text,
	campus_id text NOT NULL UNIQUE,
	average_time real
);"""

evaluations_table = """CREATE TABLE IF NOT EXISTS evaluations (
	eval_id integer NOT NULL UNIQUE,
	project_id integer NOT NULL,
	scale_id integer,
	time_start integer,
	time_end integer,
	corrected_id text NOT NULL,
	corrected_feedback text,
	corrected_rating text,
	corrector_id integer NOT NULL,
	corrector_feedback text,
	corrector_mark integer NOT NULL,
	corrector_flag text NOT NULL
);"""

"""
project_id		-> scale_team['team']['project_id']
name 			-> v2/projects filter[id] : project_id
campus_id		-> func call
average_time 	-> SELECT * FROM evaluations WHERE e.project_id = project_id
					time += eval['time']
					= time / evalutations.len()
"""

def	establish():
	connection = database_func.create_connection(database_name)
	if connection == None:
		exit()
	database_func.create_table(connection, campus_table)
	database_func.create_table(connection, students_table)
	database_func.create_table(connection, projects_table)
	database_func.create_table(connection, evaluations_table)
	return connection

if __name__ == '__main__':
	exit()
