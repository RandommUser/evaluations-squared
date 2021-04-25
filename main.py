# global
import requests, sys, json
# local
import database, helpers, database_func

# make a request to the 42 API. 
# params passed in the function call.
def API_request(token, end_point, call_params = { }):
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token }
	request_params = { 'per_page': 100} # default the page size to 100
	request_params.update(call_params)	#combine the params
	
	request = requests.get(end_point, headers=headers_token, params=request_params)
	if request.status_code == 200:
		print(end_point)
		return request
	else:
		print("Failed to make a request")
		print(request)
		print(request.headers)
		pass

# get the access token from the 42API
def get_token():
	app_token = open('app.json')	#app UID and secret from local file

	data = json.load(app_token)
	request_data = 'grant_type=client_credentials&client_id=' + data['UID'] + '&client_secret=' + data['secret']
	token = requests.post('https://api.intra.42.fr/oauth/token', request_data)
	if token.status_code == 200:
		parsed_ret = json.loads(token.text)
		return parsed_ret['access_token']
	else:
		print("API error on getting access token")
		print(token)
		print(token.headers)
		pass

# read campus data from local json file
def get_campus(campus = "Helsinki"):
	file_load = open('campus.json')
	data = json.load(file_load)
	return data[campus]

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
	print("Hello world")
	token = get_token()
	campus = get_campus()
	students = get_students(campus['id'])
	student_id = '59528,59596'
	student_ids = students_to_str(students, campus['id'])
	print(student_ids)
	helpers.print_json(campus)

	print(student_ids)
	connection = database_func.create_connection(database.database_name)
	if connection:
		database_func.create_table(connection, database.student_table)
		database_func.create_table(connection, database.campus_table)
		#database_func.insert_to_table(connection, "campus", database.campus_keys, ("13", "Helsinki"))
		connection.close()
	#exit()

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