import os
from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log

sched = BlockingScheduler()
USER_KEYS = ['COLE','DAN','ETHAN','JAKE','JUSTIN','MAX','NATHAN']

@sched.scheduled_job('cron', day_of_week='mon', hour=23, minute=0)
def kitchen_reminder():
	user = setNextBoy()
	msg = "{}, it is your kitchen week!".format(user)
	send_message(msg, user)
	return "ok", 200

def setNextBoy():
	""" sets and returns next Kitchen Boy
	"""
	currentBoy = os.getenv('KITCHEN_BOY')
	for i in range(5):
		if currentBoy == USER_KEYS[i]:
			os.environ['KITCHEN_BOY'] = USER_KEYS[i+1]
	if currentBoy == USER_KEYS[6]:
		os.environ['KITCHEN_BOY'] = USER_KEYS[0]
	return os.getenv('KITCHEN_BOY')

sched.start()