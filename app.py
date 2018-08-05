import os
import sys
import json
import requests
import psycopg2
from flask import *
from passlib.hash import pbkdf2_sha256
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)

# routes GET case to app
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

# returns JSON of all boys in db to front-end
@app.route('/select', methods=['POST'])
def select():
	boys = getAll()

	boysDict = {}
	for boy in boys:
		boysDict[boy] = getNickname(boy)

	boysJSON = jsonify(boysDict)
	return boysJSON

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
			msg = 'You can say to me:\n\nWhose week is it?\nThe kitchen is a mess!\nThe kitchen looks great!\nWhose week is it next?\nSend help!'
			send_message(msg)

		elif "whose week is next" in text:
			user = getNextBoy()
			msg = "It is {}'s week next week!".format(getNickname(user))
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

		elif ("downstairs" or "basement") and ("fridge" or "refrigerator") in text:
			msg = "That is outside my jurisdiction." 
			send_message(msg)

		elif "send help" in text:
			users = getAll()
			msg = "Help!"
			send_message(msg, users)

		# If no pre-set response, analyze general sentiment of message and return appropriate response
		else:
			msg = sentiment_analysis(text)
			send_message(msg)

	return "ok", 200

def sentiment_analysis(text):
	''' analyzes tone of message and returns appropriate response
		uses IBM Watson Tone Analyzer API
	'''

	# create tone analyzer
	try:
		tone_analyzer = ToneAnalyzerV3(
	    	version = "2017-09-21",
	    	username = os.environ["IBM_USERNAME"],
	    	password = os.environ["IBM_PASSWORD"]
		)
		tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})
	except:
		return "I'm not sure what to think! (No IBM Cloud account found)"

	# API call
	try:
		toneJSON = tone_analyzer.tone(text, 'text/plain')
	except WatsonApiException as ex:
		log("Watson API call failed with status code " + str(ex.code) + ": " + ex.message)
		return "I'm not sure what to think! (error 1: check logs)"
	else:
		detected_tones = toneJSON["document_tone"]["tones"]
		emotional_tones = []

		for tone in detected_tones:
			if tone["tone_id"] in ["anger", "fear", "joy", "sadness"]:
				emotional_tones.append(tone["tone_id"])

		# responses
		if len(emotional_tones) > 1:
			return "I'm sensing a lot of emotion from this message."
		elif len(emotional_tones) < 1:
			return "I'm not sure what to think!"
		elif emotional_tones[0] == "anger":
			return "Chill out, man."
		elif emotional_tones[0] == "fear":
			return "You're scaring me..."
		elif emotional_tones[0] == "joy":
			return "I'm just happy you're happy."
		elif emotional_tones[0] == "sadness":
			return "I'm sorry you're sad."
		else:
			log(emotional_tones)
			return "I'm not sure what to think! (error 2: check logs)"

@app.route('/custom', methods=['POST'])
def custom_message():
	web_id = request.form['web_id']
	msg = request.form['message']
	user = request.form['mention']
	web_id_hash = os.environ['WEB_ID']
	if pbkdf2_sha256.verify(web_id, web_id_hash):
		
		if user == "NONE":
			send_message(msg)
		elif user == "ALL":
			send_message(msg, getAll())
		else:
			send_message(msg, [user])

	else:
		log("Unauthorized access attempt!")

	return redirect('/')

def send_message(msg, users=[]):
	# GroupMe API
	url = 'https://api.groupme.com/v3/bots/post'
	# HTTP Post Body (will mention user if arg is given)
	if users != []:
		data = {
					'bot_id': os.environ['GROUPME_BOT_ID'],
					'text': msg,
					'attachments': [
						{
							'type': 'mentions',
							'user_ids': [str(getUserID(user)) for user in users],
					 		'loci': [[0,len(msg)] for user in users]
						}
					]
				}
	else:
		data = {
					'bot_id': os.environ['GROUPME_BOT_ID'],
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
	''' returns List of names of all boys
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy;")
	raw_boys = cur.fetchall()
	boys = [boy[0] for boy in raw_boys]
	cur.close()
	return boys

def getBoy():
	''' returns String of name of current kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy WHERE isBoy;")
	boy = cur.fetchone()[0]
	cur.close()
	return boy

def getNextBoy():
	''' reuturns String of name of next week's kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT nextboy FROM kitchen_boy WHERE isBoy;")
	nextBoy = cur.fetchone()[0]
	cur.close()
	return nextBoy

def getNickname(user):
	''' returns String of nickname of nickname of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT nickname FROM nicknames WHERE name LIKE (%s);",(user,))
	nickname = cur.fetchone()[0]
	cur.close()
	return nickname

def getUserID(user):
	''' gets String of GroupMe ID of user
	'''
	cur = conn.cursor()
	cur.execute("SELECT id FROM user_ids WHERE name LIKE (%s);",(user,))
	user_id = cur.fetchone()[0]
	cur.close()
	return user_id
