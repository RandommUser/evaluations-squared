# global
import requests, sys, json, time, sqlite3
from sqlite3 import Error
#local
import helpers, database, database_func, app

# API page lenghts. Doesn't seem to work
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
	elif table == 'evaluations' and campus != None:
		strp_formatting = "%Y-%m-%dT%H:%M:%S"
		correcteds_id = ""
		for corrected in jason['correcteds']:
			if correcteds_id != "":
				correcteds_id += ", "
			correcteds_id += str(corrected['id'])
		# yeah... this is a mess :^)
		ret = tuple((jason['id'], jason['team']['project_id'], jason['team']['id'], int(campus), \
			int(time.mktime(time.strptime(jason['begin_at'].split('.', 2)[0], strp_formatting))),\
			int(time.mktime(time.strptime(jason['created_at'].split('.', 2)[0], strp_formatting))),\
				correcteds_id, jason['feedbacks'][0]['comment'], str(jason['feedbacks'][0]['rating']), jason['corrector']['id'], jason['feedback'],\
					jason['final_mark'], jason['flag']['name']))
	elif table == 'projects' and campus != None:
		ret = tuple((jason['id'], jason['name'], campus, -1))
	else:
		return
	return ret

# save API response to a table
def API_to_table(connection, token, end_point, table, call_params = { }, campus = None):
	if connection == None:
		raise TypeError("API_to_table connection not given")
		return
	elif end_point == "" or end_point == None:
		raise TypeError("API_to_table end_point not given")
		return
	elif table == "" or table == None:
		raise TypeError("API_to_table table not given")
		return
	if token == None:
		token = get_token()
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token['access_token'] }
	request_params = { 'per_page': 30 }
	if page_lens.get(end_point) != None:	# if the end point len is listed in the dictionary replace it in the headers. Doesn't get it properly
		request_params['per_page'] = page_lens[end_point]
	request_params.update(call_params)

	page = -2
	page_max = -1
	errors = 0
	
	print(end_point)
	# loop thru all the API pages
	while page <= page_max and errors < 3:
		request = None
		values = None
		if page != -2:
			print("Page %10d/%10d" % (page, page_max))
		try:
			request = requests.get(end_point, headers=headers_token, params=request_params)
			response_parse =  json.loads(request.text)
			for jason in response_parse:
				try:
					if table == "students" and '3b3-' in jason['login']: # hardcoded bad student filter to make it not need SQL query
						continue
					values = json_to_tuple(jason, table, campus)
					if values == None:
						print("No tuple logic setup for table")
						print(table)
						return
					database_func.replace_into_table(connection, table, database.keys[table], values)
				except: # some API tuples don't work with the table from projects. Dunno why
					print("Failed to insert. skipping")
					print(database.keys[table])
					print(values)
					continue
			page = int(request.headers['X-Page'])
			if page_max == -1:
				page_max = int(request.headers['X-Total']) / int(request_params['per_page'])
				if page_max > int(page_max):
					page_max += 1
				page_max = int(page_max)
			request_params.update({ 'page' : page + 1})
		except Error as err:
			print(err)
		except:
			if request.status_code == 200:
				print("Try failed")
				print(request)
				print(values)
			elif request.status_code == 429: # too fast calls, sleep
				time.sleep(float(request.headers['Retry-After']))
			elif request.status_code == 401: # old token
				token = get_token()
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
		return request
	elif request.status_code == 401: # old token
		token = get_token()
		return API_request(token, end_point, call_params)
	else:
		print(request)
		print(request.headers)
		raise RuntimeError("Failed to make a request")
		return

# get the access token from the 42API
def get_token():
	data = app.app
	request_data = 'grant_type=client_credentials&client_id=' + data['UID'] + '&client_secret=' + data['secret']
	token = requests.post('https://api.intra.42.fr/oauth/token', request_data)
	if token.status_code == 200:
		parsed_ret = json.loads(token.text)
		# add expires_at variable to the token
		parsed_ret['expires_at'] = parsed_ret['created_at'] + parsed_ret['expires_in']
		return parsed_ret
	else:
		print("API error on getting access token")
		print(token)
		print(token.headers)
		raise RuntimeError("Failed to get the token")
		return 

if __name__ == '__main__':
	exit()
