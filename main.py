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
		elif c == '[':
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


def API_request(token, end_point):
	end_point = 'https://api.intra.42.fr/' + end_point
	headers_token = { 'Authorization': 'Bearer ' + token }
	request = requests.get(end_point, headers=headers_token)
	if request.status_code == 200:
		print(request)
		print_json(request.headers)
		#print(request.text)
		ret = json.loads(request.text)
		return ret
	else:
		print("Failed to make a request")
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
		pass

def main():
	print("Hello world")
	token = get_token()
	if token:
		print(token)
		response = API_request(token, 'oauth/token/info')
		print_json(response)
		response = API_request(token, '/v2/campus')
		print_json(response)
	else:
		exit()

if __name__ == '__main__':
	main()