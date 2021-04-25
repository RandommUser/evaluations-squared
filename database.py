# global
import sqlite3
from sqlite3 import Error


# database name
database_name = '42API.db'

# table key tuples used in insert_to_table()
campus_keys = ("campus_id", "name")
student_keys = ("user_id", "login", "campus_id", "url")


# table structures
campus_table = """CREATE TABLE IF NOT EXISTS campus (
	campus_id integer NOT NULL,
	name text NOT NULL
);"""

student_table = """CREATE TABLE IF NOT EXISTS students (
	user_id integer NOT NULL,
	login text NOT NULL,
	campus_id integer NOT NULL,
	url text NOT NULL
);"""
