# global
import sys, json

# combine two arrays of dictionaries without dupes
def combine_arr_dict(dic1, dic2):
	for ob2 in dic2:
		if ob2 not in dic1:
			dic1.append(ob2)
	return dic1

def print_db(input, keys = None, default = True):
	if keys != None:
		headers = ""
		if default == True:
			headers += "rowid"
		for key in keys:
			headers += "\t" + key
		print(headers)
	for row in input:
		row_print = ""
		for entry in row:
			row_print += str(entry) + "\t"
		print(row_print)


# print out a json string in somewhat more readable format
def print_json(input):
	tabs = 0
	in_list = 0
	in_brackets = 0
	quotes = {'big': 0, 'small': 0}
	output = ""
	stringify = ""
	if type(input) == str:	#check if input needs changing
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

if __name__ == '__main__':
	exit()
