from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log

sched = BlockingScheduler()
USER_KEYS = ['COLE','DAN','ETHAN','JAKE','JUSTIN','MAX','NATHAN']

@sched.scheduled_job('cron', day_of_week='fri', hour=20, minute=35)
def kitchen_reminder():
	user = nextBoy()
    msg = "{}, it is your kitchen week!".format(user)
    send_message(msg, user)
    log('Sent {}'.format(msg))
    return "ok", 200

def nextBoy():
	for i in range(5):
		if os.getenv('KITCHEN_BOY') == USER_KEYS[i]:
			os.putenv('KITCHEN_BOY', USER_KEYS[i+1])
	if os.getenv('KITCHEN_BOY') == USER_KEYS[6]:
		os.putenv('KITCHEN_BOY', USER_KEYS[0])

sched.start()