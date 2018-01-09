import json
import os
import re, requests

filepath = os.getcwd() + "\\..\\slackbot\\scripts\\logs"
filename = "links.txt"

# SETUP TOKEN 
# Bot User OAuth Access Token
token = os.environ['HUBOT_SLACK_TOKEN']

# SETUP CHANNEL
channel_id = "" # Give ID or leave empty string and fill out channel_name
channel_name = "test"
is_private = True

# CATEGORIES = ["grow.liferay", "web.liferay", "loop.liferay", "stackoverflow", "others", "github"]
def get_channel_id(channel, method):
	api_url = 'https://slack.com/api/{c}.{m}?token={t}&pretty=1'.format(c=channel, m=method, t=token)

	response = requests.get(api_url)
	json_data = response.json()

	for group in json_data['groups']:
		name = group['name']

		if channel_name == name:
			return group['id']

	# add error handling

def pull_slack_history():
	global channel_id

	results = {}
	output = ""
	
	channel = "channels"
	if is_private:
		channel = "groups"

	if not channel_id:
		method = "list"
		channel_id = get_channel_id(channel, method)	
	
	# add error handling
	method = "history"
	query = "channel=" + channel_id
		
	api_url = 'https://slack.com/api/{c}.{m}?token={t}&pretty=1&{q}'.format(c=channel, m=method, t=token, q=query)

	response = requests.get(api_url)
	json_data = response.json()

	for message in json_data['messages']:
		text = message['text']
		searchObject = re.search("<(https:\/\/[^\s]+)>", text) #|<(http:\/\/[^\s]+\|)

		if searchObject:
			URL = searchObject.group()[1:-1]

			if URL in results:
				if message['ts'] > results[URL]:
					results[URL] = message['ts']
			else:
				results[URL] = message['ts']

	for result in results:
		output += result + ", " + results[result] + "\n"

	write_file(filepath, filename, output)

def write_file(path, name, output):
	try:
		file = open(path + "\\" + name,"w", encoding="UTF-8")
		file.write(output)
		file.close()
		
		return True
	except IOError:
		return False

pull_slack_history()