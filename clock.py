import os
import requests
import psycopg2
import db_lib as db

from app import send_message, log
from apscheduler.schedulers.blocking import BlockingScheduler

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def kitchen_reminder():

	# fetch current status
	status = db.getStatus(conn)

	# if notify is disabled, no operation needed
	if status == "DISABLED":
		log("kitchen_reminder trigger; bot NOTIFY_STATUS is disabled")
		return "ok", 200

	currentBoyNum = db.getBoyNum(conn)

	# if first day has passed
	if currentBoyNum == 1:

		# increment day
		currentBoy = db.getBoy(conn)
		db.changeDay(conn, currentBoy)

	# if second day has passed
	elif currentBoyNum == 2:
		
		# pass responsiblity
		currentBoy = db.getBoy(conn)
		nextBoy = db.getNextBoy(conn)
		db.updateBoy(conn, currentBoy, nextBoy)
		
		# send message to new kitchen boy
		msg = "{}, it is your kitchen day!".format(db.getNickname(conn, nextBoy))
		send_message(msg, [nextBoy])

	else:
		log("Error: getBoyNum() returned an unexpected value: {}".format(currentBoyNum))
	
	return "ok", 200

def rent_reminder():
	msg = "Don't forget to pay rent!"
	send_message(msg, db.getAll(conn))
	return "ok", 200

sched = BlockingScheduler()
sched.add_job(kitchen_reminder, 'cron', hour=0, minute=0)
sched.add_job(rent_reminder, 'cron', day=1)
sched.start()
