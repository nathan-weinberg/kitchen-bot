import os
import requests
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log, getBoy, getNextBoy, getNickname, getAll, getBoyNum

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def kitchen_reminder():
	currentBoyNum = getBoyNum()

	# fire if today is rollover day
	if currentBoyNum == 2:
		
		# pass responsiblity
		currentBoy = getBoy()
		nextBoy = getNextBoy()
		updateBoy(currentBoy, nextBoy)
		
		# send message to new kitchen boy
		msg = "{}, it is your kitchen day!".format(getNickname(nextBoy))
		send_message(msg, [nextBoy])
		return "ok", 200

def rent_reminder():
	msg = "Don't forget to pay rent!"
	send_message(msg, getAll())
	return "ok", 200

def change_day(num):
	''' changes dayNum attribute for current boy
	'''

	cur = conn.cursor()
	currentBoy = getBoy()

	# changes dayNum variable of currentBoy in kitchen_boy table to num
	cur.execute("UPDATE kitchen_boy SET dayNum = {} WHERE name LIKE {};".format(num, currentBoy))

	# commit changes
	conn.commit()
	cur.close()

def updateBoy(prevBoy,nextBoy):
	''' passes responsiblity of kitchen boy
	'''	
	cur = conn.cursor()

	# erase responsibility from previous boy
	cur.execute("UPDATE kitchen_boy SET isBoy = false WHERE name LIKE {}};".format(prevBoy))
	# reset day number of previous boy
	cur.execute("UPDATE kitchen_boy SET dayNum = 1 WHERE name LIKE {};".format(prevBoy))
	# assign responsibility to next boy
	cur.execute("UPDATE kitchen_boy SET isBoy = true WHERE name LIKE {};".format(nextBoy))
	
	# commit changes
	conn.commit()
	cur.close()

sched = BlockingScheduler()
sched.add_job(kitchen_reminder, 'cron', hour=0, minute=15)
sched.add_job(change_day, 'cron', [2], day='*/2', hour=0, minute=30)
sched.add_job(rent_reminder, 'cron', day=1)
sched.start()
