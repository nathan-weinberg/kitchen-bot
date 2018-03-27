import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log, getBoy, 

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon', hour=0, minute=0)
def kitchen_reminder():
	user = nextBoy()
	msg = "{}, it is your kitchen week!".format(getNickname(user))
	send_message(msg, user)
	return "ok", 200

### database interaction functions ###

def nextBoy():
	""" sets and returns next Kitchen Boy
	"""
	cur = conn.cursor()

	# update db tables
	currentBoy = getBoy()
	nextBoy = nextBoy()
	updateBoy(currentBoy,nextBoy)

	cur.close()
	return nextBoy

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

sched.start()