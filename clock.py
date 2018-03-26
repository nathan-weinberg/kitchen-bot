import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

sched = BlockingScheduler()
USER_KEYS = ['COLE','DAN','ETHAN','JAKE','JUSTIN','MAX','NATHAN']

@sched.scheduled_job('cron', day_of_week='mon', hour=0, minute=6)
def kitchen_reminder():
	user = nextBoy()
	nickname = getNickname(user)
	msg = "{}, it is your kitchen week!".format(nickname)
	send_message(msg, user)
	return "ok", 200

### database interaction functions ###

def nextBoy():
	""" sets and returns next Kitchen Boy
	"""
	cur = conn.cursor()

	# update db tables
	currentBoy = getBoy()
	for i in range(5):
		if currentBoy == USER_KEYS[i]:
			nextBoy = USER_KEYS[i+1]
	if currentBoy == USER_KEYS[6]:
		nextBoy = USER_KEYS[0]
	updateBoy(currentBoy,nextBoy)

	cur.close()
	return nextBoy

def getBoy():
	''' gets name of current kitchen boy
	'''
	cur = conn.cursor()
	cur.execute("SELECT name FROM kitchen_boy WHERE isBoy;")
	boy = cur.fetchone()[0]
	cur.close()
	return boy

def updateBoy(prevBoy,nextBoy):
	''' passes responsiblity of kitchen boy
	'''	
	cur = conn.cursor()

	# erase responsibility from previous boy
	cur.execute("UPDATE kitchen_boy SET isBoy = false WHERE name LIKE (%s);",(prevBoy,))
	# assign responsibility to next boy
	cur.execute("UPDATE kitchen_boy SET isBoy = true WHERE name LIKE (%s);",(nextBoy,))
	
	# commit changes
	conn.commit()
	cur.close()

def getNickname(user):
	cur = conn.cursor()
	cur.execute("SELECT nickname FROM nicknames WHERE name LIKE (%s);",(user,))
	nickname = cur.fetchone()[1]
	cur.close()
	return nickname

sched.start()