import os
import sys
import json
import requests
from flask import *

app = Flask(__name__)

# routes GET case to app
@app.route('/', methods=['GET'])
def index():
	return "KitchenBot is online."

# routes POST case to app (occurs when new message to GroupMe is sent by any user)
@app.route('/', methods=['POST'])
def webhook():

	# decode JSON data
	data = request.get_json()
	log('Received {}'.format(data))

	# detect whether or not KitchenBot is being addressed in message
	if "@KitchenBot" in data['text']:
		msg = "Hey {}, I see you addressed me but I'm too dumb to know what you're saying right now!".format(data['name'])
		send_message(msg)

	return "ok", 200

def send_message(msg, user=None):
	# GroupMe API
	url = 'https://api.groupme.com/v3/bots/post'
	# HTTP Post Body (will mention user if arg is given)
	if user != None:
		data = {'bot_id': os.getenv('GROUPME_BOT_ID'), 'text': msg, 'attachments': [{'type': 'mentions', 'user_ids': [os.getenv(user)]}]}
	else:
		data = {'bot_id': os.getenv('GROUPME_BOT_ID'), 'text': msg}
	# HTTP Post 
	resp = requests.post(url, json=data)

def log(msg):
	print(str(msg))
	sys.stdout.flush()