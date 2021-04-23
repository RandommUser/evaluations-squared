import requests, sys, json

def print_json(input):
	tabs = 0
	in_list = 0
	in_brackets = 0
	quotes = {'big': 0, 'small': 0}
	output = ""
	stringify = ""
	if type(input) == str:
		stringify = input
	elif type(input) == dict:
		stringify = json.dumps(input)
	else:
		stringify = str(input)
	for c in stringify:
		if c == '{':
			tabs += 1
			output += c
			print(output)
			output = "\t" * tabs
			in_brackets += 1
		elif c == '}':
			print(output)
			tabs -= 1
			in_brackets -= 1
			output = "\t" * tabs
			output += c
			if in_brackets == 0:
				print(output)
				output = "\t" * tabs
		elif c == '[' and in_brackets != 0:
			in_list += 1
			output += c
		elif c == ']':
			in_list -= 1
			output += c
		elif c == '"' and quotes['big'] == 0:
			output += c
			quotes['big'] += 1
		elif c == '"' and quotes['big'] != 0:
			output += c
			quotes['big'] -= 1
		elif c == "'" and quotes['small'] == 0:
			output += c
			quotes['small'] += 1
		elif c == "'" and quotes['small'] != 0:
			output += c
			quotes['small'] -= 1
		elif c == ',' and in_list == 0 and quotes['small'] == 0 and quotes['big'] == 0:
			output += c
			print(output)
			output = "\t" * tabs
		else:
			output += c


def API_request(token, end_point, call_params = { }):
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token }
	request_params = { 'per_page': 100}
	request_params.update(call_params)
	
	request = requests.get(end_point, headers=headers_token, params=request_params)
	if request.status_code == 200:
		print(end_point)
		return request
	else:
		print("Failed to make a request")
		print(request)
		print(request.headers)
		pass

def get_token():
	app_token = open('app.json')

	data = json.load(app_token)
	#print(data)
	request_data = 'grant_type=client_credentials&client_id=' + data['UID'] + '&client_secret=' + data['secret']
	#print(request_data)
	token = requests.post('https://api.intra.42.fr/oauth/token', request_data)
#	print(token.status_code)
	if token.status_code == 200:
		#print(token.text)
		parsed_ret = json.loads(token.text)
		return parsed_ret['access_token']
	else:
		print("API error on getting access token")
		print(token)
		print(token.headers)
		pass

def get_campus(campus = "Hive"):
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

def get_students(id):
	if type(id) != str:
		id = str(id)
	file_load = open('users.json')
	data = json.load(file_load)
	for campus in data: # remove students with bad id
		data[str(campus)] = exclude_bad_logins(data[str(campus)])
	return data

def combine_arr_dict(dic1, dic2):
	for ob2 in dic2:
		if ob2 not in dic1:
			dic1.append(ob2)
	return dic1

def print_more_students(students, campus_id):
	campus_id = str(campus_id)
	response = API_request(token, 'v2/users', {'campus_id' : campus_id, 'page' : 1})
	print_json(response.headers)
	cleaned_array = json.loads(response.text)
	students[campus_id] = combine_arr_dict(students[campus_id], cleaned_array)
	with open('users.json', 'w') as outfile:
		json.dump(data, outfile)

def students_to_str(students, campus_id):
	invalid = [ '3b3-']
	ret = ['']
	rlen = 0
	i = 0
	for student in students[str(campus_id)]:
		#if '3b3-' in str(student['login']):
		#	continue
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
	print_json(campus)

	print(student_ids)
	exit()

	if token:
		print(token)

		#response = API_request(token, 'v2/campus', { 'page': 2, 'per_page' : 30})

		#response = API_request(token, 'v2/scale_teams', { 'page': 423395, 'per_page': 5})
		response = API_request(token, 'v2/scale_teams', { 'page': 1, 'per_page': 30, 'filter[user_id]' : student_ids[0], \
			'range[created_at]' : '2021-04-01,2021-04-23'})
		if response:
			print_json(response.text)
			print_json(response.headers)
		#print(student_ids)
	else:
		exit()

if __name__ == '__main__':
	main()