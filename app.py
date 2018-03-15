import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# routes case to app when message to GroupMe is sent
@app.route('/', methods=['POST'])
def webhook():

	# decode JSON data
	data = request.get_json()
	log('Received {}'.format(data))

	# prevent bot from quoting itself
	if data['name'] != 'KitchenBot':
		msg = '{}, you sent "{}".'.format(data['name'], data['text'])
		send_message(msg)

	return "ok", 200

def send_message(msg):
	# GroupMe API
	url = 'https://api.groupme.com/v3/bots/post'
	# HTTP Post Body
	data = {'bot_id': os.getenv('GROUPME_BOT_ID'), 'text': msg}
	# HTTP Post 
	resp = requests.post(url, json=data)

def log(msg):
	print(str(msg))
	sys.stdout.flush()