# global
import requests, sys, json, time, calendar
#local
import helpers, database, database_func

page_lens = {
	"v2/campus" : 30,
	"v2/users" : 100,
	"v2/scale_teams" : 30,
}

# read from 42API response to create a tuple based on the campus to be used for database insertion
def json_to_tuple(jason, table, campus = None):
	if type(jason) != dict:
		return
	if table == 'campus':
		ret = tuple((jason['id'], jason['name']))
	elif table == 'students' and campus != None:
		ret = tuple((jason['id'], jason['login'], campus, jason['url']))
	else:
		return
	return ret

def API_to_table(connection, token, end_point, table, call_params = { }, campus = None):
	if connection == None:
		print("API_to_table connection not given")
		return
	elif end_point == "" or end_point == None:
		print("API_to_table end_point not given")
		return
	elif table == "" or table == None:
		print("API_to_table table not given")
		return
	if token == None:
		token = get_token()
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token['access_token'] }
	request_params = { 'per_page': 30 }
	if page_lens.get(end_point) != None:	# if the end point len is listed in the dictionary replace it in the headers
		request_params['per_page'] = page_lens[end_point]
	request_params.update(call_params)

	page = -2
	page_max = -1
	errors = 0
	
	print("request loop")
	while page <= page_max and errors < 3:
		print(page)
		print(request_params)
		request = requests.get(end_point, headers=headers_token, params=request_params)
		if request.status_code == 200:
			response_parse =  json.loads(request.text)
			for jason in response_parse:
				if table == "students" and '3b3-' in jason['login']: # hardcoded bad student filter
					continue
				values = json_to_tuple(jason, table, campus)
				if values == None:
					print("No tuple logic setup for table")
					print(table)
					return
				database_func.replace_into_table(connection, table, database.keys[table], values)
			page = int(request.headers['X-Page'])
			if page_max == -1:
				page_max = int(request.headers['X-Total']) / int(request_params['per_page'])
				if page_max > int(page_max):
					page_max += 1
				page_max = int(page_max)
			request_params.update({ 'page' : page + 1})
		else:
			helpers.print_json(request.headers)
			errors += 1





# make a request to the 42 API. 
# params passed in the function call.
def API_request(token, end_point, call_params = { }):
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token['access_token'] }
	request_params = { 'per_page': 100} # default the page size to 100
	request_params.update(call_params)	#combine the params
	
	request = requests.get(end_point, headers=headers_token, params=request_params)
	if request.status_code == 200:
		print(end_point)
		print(request_params)
		return request
	else: # 401 if old token
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
		parsed_ret['expires_at'] = parsed_ret['created_at'] + parsed_ret['expires_in']
		helpers.print_json(parsed_ret)
		print(int(time.time()))#calendar.timegm(time.gmtime()))
		print(token.headers)
		return parsed_ret
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

if __name__ == '__main__':
	exit()
