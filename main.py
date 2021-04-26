# global
import requests, sys, json
# local
import database, helpers, database_func, api42

# get array dict. removes bad logins from the list
def exclude_bad_logins(student_array):
	res = []
	for student in student_array:
		if '3b3-' not in student['login']:
			res.append(student)
	return res

# get student array dict from local json based on the request campus_id
def get_students(id):
	if type(id) != str:
		id = str(id)
	file_load = open('users.json')
	data = json.load(file_load)
	for campus in data: # remove students with bad id
		data[str(campus)] = exclude_bad_logins(data[str(campus)])
	return data

# print out more students in the students.json file
# no dupes, manually more pages from API
def print_more_students(students, campus_id):
	campus_id = str(campus_id)
	response = API_request(token, 'v2/users', {'campus_id' : campus_id, 'page' : 1})
	helpers.print_json(response.headers)
	cleaned_array = json.loads(response.text)
	students[campus_id] = helpers.combine_arr_dict(students[campus_id], cleaned_array)
	with open('users.json', 'w') as outfile:
		json.dump(data, outfile)

# create a user_id string for campus based filter for API calls.
# use array to split it, from testing the filter limit is 186 ids on one request
def students_to_str(students, campus_id):
	ret = ['']
	rlen = 0
	i = 0
	for student in students[str(campus_id)]:
		if ret[i] != '':
			ret[i] += ','
		ret[i] += str(student['id'])
		rlen += 1
		if rlen > 186:
			rlen = 0
			i += 1
			ret.append('')
	print(ret)
	return ret

def main():
	token = api42.get_token()
	#ret = api42.API_request(token['access_token'], 'v2/scale_teams', { 'page': 1, 'per_page' : 1})
	#helpers.print_json(ret.headers)
	#exit()
	connection = database_func.create_connection(database.database_name)
	if connection:
		database_func.create_table(connection, database.students_table)
		database_func.create_table(connection, database.campus_table)
		"""
		ret = database_func.replace_into_table(connection, "campus", database.campus_keys, ("14", "New York"))
		print(ret)
		ret = database_func.select_all_table(connection, "campus", database.campus_keys)
		print(ret)
		ret = database_func.select_from_table(connection, "campus", database.campus_keys, tuple(("campus_id =", "name =")), tuple(("13", "Paris")), "OR")
		print(ret)
		print(len(ret))
		"""
		#api42.API_to_table(connection, token, "v2/campus", "campus")
		db = "students"
		#api42.API_to_table(connection, token, "v2/users", db, { 'campus_id' : '13' }, 13)
		database_func.delete_where(connection, db, (("login LIKE",)), (("3b3-%",)))
		ret = database_func.select_all_table(connection, db, database.keys[db])
		helpers.print_db(ret, database.keys[db])
		connection.close()
	exit()

	if token:
		print(token)

		#response = API_request(token, 'v2/campus', { 'page': 2, 'per_page' : 30})

		#response = API_request(token, 'v2/scale_teams', { 'page': 423395, 'per_page': 5})
		"""response = API_request(token, 'v2/scale_teams', { 'page': 1, 'per_page': 1, 'filter[user_id]' : student_ids[0], \
			'range[created_at]' : '2021-04-01,2021-04-23'})"""
		response = API_request(token, 'v2/feedbacks', { 'scale_team_id': 3151573, 'page': 1, 'per_page': 1 })
		if response:
			helpers.print_json(response.text)
			helpers.print_json(response.headers)
		#print(student_ids)
	else:
		exit()

if __name__ == '__main__':
	main()