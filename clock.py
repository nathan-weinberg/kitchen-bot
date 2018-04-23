import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log, getBoy, getNextBoy, getNickname

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon', hour=8, minute=10)
def kitchen_reminder():
	currentBoy = getBoy()
	nextBoy = getNextBoy()
	msg = "{}, it is your kitchen week!".format(getNickname(nextBoy))

	updateBoy(currentBoy, nextBoy)
	send_message(msg, [nextBoy])
	return "ok", 200

### database interaction functions ###

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