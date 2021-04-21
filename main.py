import requests, sys, json

def get_token():
	app_token = open('app.json')

	data = json.load(app_token)
	print(data)
	request_data = 'grant_type=client_credentials&client_id=' + data['UID'] + '&client_secret=' + data['secret']
	print(request_data)
	token = requests.post('https://api.intra.42.fr/oauth/token', request_data)
	print(token.status_code)
#	print(token.headers)
	print(token.text)
#	print(token.links)
#	print(token.content)

def main():
	print("Hello world")
	get_token()

if __name__ == '__main__':
	main()