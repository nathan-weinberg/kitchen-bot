import os
import sys
import json
import requests
import psycopg2
from flask import *

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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
		if "what can i say to you" in text:
			msg = 'You can say to me:\n\nWhose week is it?\nThe kitchen is a mess!\nThe kitchen looks great!\nWhose week is it next?'
			send_message(msg)
		elif "whose week is it" in text:
			user = getBoy()
			msg = "It is {}'s week!".format(getNickname(user))
			send_message(msg)
		elif "the kitchen is a mess" in text:
			user = getBoy()
			msg = "{}, clean the kitchen!".format(getNickname(user))
			send_message(msg, [user])
		elif "the kitchen looks great" in text:
			user = getBoy()
			msg = "Great job with the kitchen {}!".format(getNickname(user))
			send_message(msg, [user])
		elif "whose week is next" in text:
			user = getNextBoy()
			msg = "It is {}'s week next week!".format(getNickname(user))
			send_message(msg)
		elif ("downstairs" or "basement") and ("fridge" or "refrigerator") in text:
			msg = "That is outside my jurisdiction." 
			send_message(msg)
		elif "send help" in text:
			users = getAll()
			msg = "Help!"
			send_message(msg, users)
		else:
			msg = "Hey {}, I see you addressed me but I'm too dumb to know what you're saying right now!".format(data['name'])
			send_message(msg)

	return "ok", 200

def send_message(msg, users=[]):
	# GroupMe API
	url = 'https://api.groupme.com/v3/bots/post'
	# HTTP Post Body (will mention user if arg is given)
	if users != []:
		data = {
					'bot_id': os.getenv('GROUPME_BOT_ID'),
					'text': msg,
					'attachments': [
						{
							'type': 'mentions',
							'user_ids': [str(getUserID(user)) for user in users],
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
	log('Sent {}'.format(data))

def log(msg):
	print(str(msg))
	sys.stdout.flush()

### database interaction functions ###

def getAll():
	''' gets names of all boys
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy;")
	raw_boys = cur.fetchall() # fetchall names, put in list
	boys = [boy[0] for boy in raw_boys]
	cur.close()
	return boys

def getBoy():
	''' gets name of current kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy WHERE isBoy;")
	boy = cur.fetchone()[0]
	cur.close()
	return boy

def getNextBoy():
	''' gets name of next week's kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT nextboy FROM kitchen_boy WHERE isBoy;")
	nextBoy = cur.fetchone()[0]
	cur.close()
	return nextBoy

def getNickname(user):
	''' gets nickname of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT nickname FROM nicknames WHERE name LIKE (%s);",(user,))
	nickname = cur.fetchone()[0]
	cur.close()
	return nickname

def getUserID(user):
	''' gets id of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT id FROM user_ids WHERE name LIKE (%s);",(user,))
	user_id = cur.fetchone()[0]
	cur.close()
	return user_id