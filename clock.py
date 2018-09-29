import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log, getBoy, getNextBoy, getNickname, getAll

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def kitchen_reminder():
	currentBoy = getBoy()
	nextBoy = getNextBoy()
	msg = "{}, it is your kitchen day!".format(getNickname(nextBoy))

	updateBoy(currentBoy, nextBoy)
	send_message(msg, [nextBoy])
	return "ok", 200

def rent_reminder():
	msg = "Don't forget to pay rent!"
	send_message(msg, getAll())
	return "ok", 200

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

sched = BlockingScheduler()
sched.add_job(kitchen_reminder, 'cron', day='*/2', hour=0, minute=30)
sched.add_job(rent_reminder, 'cron', day=1)
sched.start()
