# global
import sqlite3, time
from sqlite3 import Error
# local
import database_func, api42, helpers


# database name
database_name = '42API.db'

# setup default values
# campus 13 is Hive Helsinki id
# eval_time_range is the time from now - eval_time_range to fetch evaluations from the campus students
setup = {
	"campus" : "13",
	"eval_time_range" : 60 * 60 * 24 * 365
}

# table key tuples used in insert_to_table()
keys = {
	"campus" : tuple(("campus_id", "name")),
	"students" : tuple(("user_id", "login", "campus_id", "url")),
	"projects_update" : tuple(("project_id", "campus_id", "average_time")),
	"projects" : tuple(("project_id", "name", "campus_id", "average_time")),
	"evaluations" : tuple(("eval_id", "project_id", "scale_id", "campus_id", "time_start", \
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
	campus_id text NOT NULL,
	average_time real,
	UNIQUE(project_id, campus_id)
);"""

evaluations_table = """CREATE TABLE IF NOT EXISTS evaluations (
	eval_id integer NOT NULL UNIQUE,
	project_id integer NOT NULL,
	scale_id integer,
	campus_id integer,
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

# used to setup the campus data. Takes a long time
def setup_db(connection, token):
	if setup.get('campus') == None:
		raise TypeError("Setup { campus : X } missing")
		return
	elif setup.get('eval_time_range') == None:
		raise TypeError("Setup { eval_time_range : X } missing")
		return
	elif type(setup['campus']) != str:
		setup['campus'] = str(setup['campus'])
	if token.get('access_token') == None:
		raise TypeError("Invalid token")
		return
	try:
		# load up the campus data
		api42.API_to_table(connection, token, "v2/campus", "campus", { 'filter[id]' : setup['campus'] })
		# load up the student data
		api42.API_to_table(connection, token, "v2/users", "students", { 'campus_id' : setup['campus'] }, setup['campus'])
		# get students in string array for eval requests
		students = database_func.get_students_arr(connection, "13")
		# make time string for range
		current_time = int(time.time())
		start_time = current_time - setup['eval_time_range']
		current_time = time.localtime(current_time)
		start_time = time.localtime(start_time)
		current_time = time.strftime("%Y-%m-%d", current_time)
		start_time = time.strftime("%Y-%m-%d", start_time)
		time_range = start_time + "," + current_time
		for arr in students:
			api42.API_to_table(connection, token, "v2/scale_teams", "evaluations", { 'filter[user_id]' : arr, 'range[created_at]' : time_range }, setup['campus'])
		# Get array of unique projects in the campus
		projects = database_func.select_distinct(connection, "evaluations", "project_id")
		project_str = ""
		project_arr = []
		# limit array size
		limit = 50
		i = 0
		for project in projects:
			if project_str != "":
				project_str += ","
			project_str += str(project[0])
			i += 1
			if i >= limit:
				project_arr.append(project_str)
				project_str = ""
				i = 0
		project_arr.append(project_str)
		for proj in project_arr:
			api42.API_to_table(connection, token, "v2/projects", "projects", { 'filter[id]' : proj }, setup['campus'])
		# Get average times for projects
		database_func.project_average(connection, setup['campus'])
	except:
		print("setup_db failed at campus")
		return

def	establish():
	try:
		connection = database_func.create_connection(database_name)
	except:
		print("Failed to make database connection. Exiting")
		exit()
	database_func.create_table(connection, campus_table)
	database_func.create_table(connection, students_table)
	database_func.create_table(connection, projects_table)
	database_func.create_table(connection, evaluations_table)
	return connection

if __name__ == '__main__':
	exit()
