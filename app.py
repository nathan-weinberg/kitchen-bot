import os
import sys
import json
import requests

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log('Recieved {}'.format(data))

	if data['name'] != 'KitchenBot':
		msg = '{}, you sent "{}".'.format(data['name'], data['text'])
		send_message(msg)

	return "ok", 200

def send_message(msg):
	url = 'https://api.groupme.com/v3/bots/post'

	data = {
			'bot_id' : os.getenv('GROUPME_BOT_ID'),
			'text'   : msg,
			}

	resp = requests.post(url, data=data)

def log(msg):
	print(str(msg))
	sys.stdout.flush()