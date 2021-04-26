# global
import sqlite3
from sqlite3 import Error


# database name
database_name = '42API.db'

# table key tuples used in insert_to_table()
keys = {
	"campus" : tuple(("campus_id", "name")),
	"students" : tuple(("user_id", "login", "campus_id", "url"))
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

if __name__ == '__main__':
	exit()
