import os
import sys
import json
import time
import datetime
import requests
import psycopg2
import database as db

from flask import *
from passlib.hash import pbkdf2_sha256
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
status = os.environ['NOTIFY_STATUS']

# routes GET case to app (occurs when webpage is accessed)
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html", status=status)

# returns JSON of all boys in db to front-end (occurs automatically when webpage is loaded)
@app.route('/select', methods=['POST'])
def select():
	boys = db.getAll(conn)

	boysDict = {}
	for boy in boys:
		boysDict[boy] = db.getNickname(conn, boy)

	boysJSON = jsonify(boysDict)
	return boysJSON

# returns JSON of all boys in db to front-end (occurs automatically when webpage is loaded)
@app.route('/schedule', methods=['POST'])
def schedule():
	data = db.getSchedule(conn)

	# replace tuples with raw names to tuples with nicknames
	for i in range(len(data)):

		# if this tuple is not current boy then do not pass on day number
		if not data[i][1]:
			data[i] = (db.getNickname(conn, data[i][0]), data[i][1], db.getNickname(conn, data[i][2]), "-")
		else:
			data[i] = (db.getNickname(conn, data[i][0]), data[i][1], db.getNickname(conn, data[i][2]), data[i][3])

	dataJSON = jsonify(data)
	return dataJSON

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
		if ("what can i say to you" in text) or ("what can i ask you" in text):
			msg = "You can say to me:\n\n" \
					"Whose day is it?\n" \
					"Whose day is next?\n" \
					"The kitchen is a mess!\n" \
					"The kitchen looks great!\n" \
					"Report status.\n" \
					"Send help!"
			send_message(msg)

		elif ("whose day is next" in text) or ("who is next" in text):

			user = db.getNextBoy(conn)
			dayNum = db.getBoyNum(conn)

			if status == 'DISABLED':
				msg = "Kitchen duty is currently inactive."
			elif dayNum == 1:
				dayAfterTomorow = datetime.date.today() + datetime.timedelta(days=2)
				msg = "It will be {}'s day on {}!".format(
					db.getNickname(conn, user),
					dayAfterTomorow.strftime("%A")
				)
			elif dayNum == 2:
				msg = "It will be {}'s day tomorow!".format(db.getNickname(conn, user))
			else:
				msg = "I'm not quite sure."
				log("Error: getBoyNum() returned an unexpected int: {}".format(dayNum))

			send_message(msg)

		elif "whose day is it" in text:
			user = db.getBoy(conn)
			dayNum = db.getBoyNum(conn)

			if status == 'DISABLED':
				msg = "Kitchen duty is currently inactive."
			elif dayNum == 1:
				today = datetime.date.today()
				tomorow = datetime.date.today() + datetime.timedelta(days=1)
				msg = "It is {}'s day today, {}, and tomorow, {}!".format(
					db.getNickname(conn, user),
					today.strftime("%A"),
					tomorow.strftime("%A")
				)
			elif dayNum == 2:
				today = datetime.date.today()
				msg = "It is {}'s day today, {}!".format(
					db.getNickname(conn, user),
					today.strftime("%A")
				)
			else:
				msg = "I'm not quite sure."
				log("Error: getBoyNum() returned an unexpected int: {}".format(dayNum))

			send_message(msg)

		elif "the kitchen is a mess" in text:

			if status == 'DISABLED':
				msg = "Kitchen duty is currently inactive."
			else:
				user = db.getBoy(conn)
				msg = "{}, clean the kitchen!".format(db.getNickname(conn, user))
			send_message(msg, [user])

		elif "the kitchen looks great" in text:
			if status == 'DISABLED':
				msg = "Kitchen duty is currently inactive."
			else:
				user = db.getBoy(conn)
				msg = "Great job with the kitchen {}!".format(db.getNickname(conn, user))
			send_message(msg, [user])

		elif ("downstairs" or "basement") and ("fridge" or "refrigerator") in text:
			msg = "That is outside my jurisdiction." 
			send_message(msg)

		elif "send help" in text:
			users = db.getAll(conn)
			msg = "Help!"
			send_message(msg, users)

		elif "report status" in text:
			if status == "DISABLED":
				msg = "Kitchen duty is suspended."
			else:
				msg = "Kitchen duty is active."
			send_message(msg)

		elif "suspend kitchen duty" in text:
			if data['sender_id'] != str(db.getUserID(conn, 'NATHAN')):
				msg = "You are not authorized to make that command."
			elif status == "DISABLED":
				msg = "Kitchen duty is already suspended."
			else:
				os.environ['NOTIFY_STATUS'] = "DISABLED"
				msg = "Kitchen duty suspended."
			send_message(msg)

		elif "resume kitchen duty" in text:
			if data['sender_id'] != str(db.getUserID(conn, 'NATHAN')):
				msg = "You are not authorized to make that command."
			elif status == "ENABLED":
				msg = "Kitchen duty is currently active."
			else:
				os.environ['NOTIFY_STATUS'] = "ENABLED"
				msg = "Kitchen duty resumed."
			send_message(msg)			

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
	    	password = os.environ["IBM_PASSWORD"],
	    	url="https://gateway.watsonplatform.net/tone-analyzer/api"
		)
		tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})
	except:
		return "I'm not sure what to think! (No IBM Cloud account found)"

	# API call
	try:
		toneJSON = tone_analyzer.tone(text, 'text/plain').get_result()
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
			send_message(msg, db.getAll(conn))
		else:
			send_message(msg, [user])
		flash("Message Sent!")

	else:
		flash("Incorrect Web ID")
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
							'user_ids': [str(db.getUserID(conn, user)) for user in users],
					 		'loci': [[0,len(msg)] for user in users]
						}
					]
				}
	else:
		data = {
					'bot_id': os.environ['GROUPME_BOT_ID'],
					'text': msg
				}
	# sleep 1 second before sending message
	time.sleep(1)
	# HTTP Post 
	resp = requests.post(url, json=data)	
	log('Sent {}'.format(data))

def log(msg):
	print(str(msg))
	sys.stdout.flush()
