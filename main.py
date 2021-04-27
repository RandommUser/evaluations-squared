# global
import sys
# local
import database, helpers, database_func, api42

def main():
	try:
		token = api42.get_token()
		connection = database.establish()
		database.setup_db(connection, token)
	except:
		print("Error")
		if connection != None:
			connection.close()
	finally:
		exit()

if __name__ == '__main__':
	main()