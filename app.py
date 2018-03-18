import os
import sys
import json
import requests
from flask import *
from clock import getNextBoy

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
	text = data['text'].lower()

	# detect whether or not KitchenBot is being addressed in message
	if "@kitchenbot" in text:
		# construct and send response
		parse_and_send(text)
	
	return "ok", 200

def parse_and_send(text):
	""" Checks for key phrases and responses in 
		appropriate manner
	"""
	if "what can i say to you" in text:
		msg = 'You can say to me:\n\nWhose week is it?\nThe kitchen is a mess!\nThe kitchen looks great!\nWhose week is it next?'
		send_message(msg)
	elif "whose week is it" in text:
		msg = "It is {}'s week!".format(os.getenv('KITCHEN_BOY'))
		send_message(msg)
	elif "the kitchen is a mess" in text:
		user = os.getenv("KITCHEN_BOY")
		msg = "{}, clean the kitchen!".format(user)
		send_message(msg, user)
	elif "the kitchen looks great" in text:
		user = os.getenv("KITCHEN_BOY")
		msg = "Great job with the kitchen {}!".format(user)
		send_message(msg, user)
	elif "whose week is it next" in text:
		msg = "It is {}'s week next week!".format(getNextBoy())
		send_message()
	else:
		msg = "Hey {}, I see you addressed me but I'm too dumb to know what you're saying right now!".format(data['name'])
		send_message(msg)

def send_message(msg, user=None):
	# GroupMe API
	url = 'https://api.groupme.com/v3/bots/post'
	# HTTP Post Body (will mention user if arg is given)
	if user != None:
		data = {
					'bot_id': os.getenv('GROUPME_BOT_ID'),
					'text': msg,
					'attachments': [
						{
						'type': 'mentions',
						'user_ids': [os.getenv(user)],
					 	'loci': [[0,len(msg)]]
						}
					]
				}
	else:
		data = {
					'bot_id': os.getenv('GROUPME_BOT_ID'),
					'text': msg
				}
	# HTTP Post 
	resp = requests.post(url, json=data)
	log('Sent {}'.format(msg))

def log(msg):
	print(str(msg))
	sys.stdout.flush()