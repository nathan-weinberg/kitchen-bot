import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log, getBoy, getNextBoy, getNickname, getAll, getBoyNum

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def kitchen_reminder():

	currentBoyNum = getBoyNum()
	log("Function triggered: getBoyNum got value: {}".format(currentBoyNum))

	# fire if first day has passed
	if currentBoyNum == 1:

		# increment day
		currentBoy = getBoy()
		changeDay(currentBoy)
		log("Changed Day")

	# fire if second day has passed
	elif currentBoyNum == 2:
		
		# pass responsiblity
		currentBoy = getBoy()
		nextBoy = getNextBoy()
		updateBoy(currentBoy, nextBoy)
		log("Passed responsiblity")
		
		# send message to new kitchen boy
		msg = "{}, it is your kitchen day!".format(getNickname(nextBoy))
		send_message(msg, [nextBoy])

	else:
		log("Error: getBoyNum() returned an unexpected value: {}".format(currentBoyNum))
	
	return "ok", 200

def rent_reminder():
	msg = "Don't forget to pay rent!"
	send_message(msg, getAll())
	return "ok", 200

def changeDay(boy):
	''' changes dayNum attribute to 2 for given boy
	'''

	cur = conn.cursor()

	# changes dayNum variable of currentBoy in kitchen_boy table to num
	cur.execute("UPDATE kitchen_boy SET dayNum = 2 WHERE name LIKE (%s);",(boy,))

	# commit changes
	conn.commit()
	cur.close()

def updateBoy(prevBoy, nextBoy):
	''' passes responsiblity of kitchen boy
	'''	
	cur = conn.cursor()

	# erase responsibility from previous boy
	cur.execute("UPDATE kitchen_boy SET isBoy = false WHERE name LIKE (%s);",(prevBoy,))
	# reset day number of previous boy
	cur.execute("UPDATE kitchen_boy SET dayNum = 1 WHERE name LIKE (%s);",(prevBoy,))
	# assign responsibility to next boy
	cur.execute("UPDATE kitchen_boy SET isBoy = true WHERE name LIKE (%s);",(nextBoy,))
	
	# commit changes
	conn.commit()
	cur.close()

sched = BlockingScheduler()
sched.add_job(kitchen_reminder, 'cron', hour=0, minute=15)
sched.add_job(rent_reminder, 'cron', day=1)
sched.start()
