from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message, log

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='fri', hour=0, minute=15)
def kitchen_reminder():
    msg = "This is a test kitchen reminder! Soon I will tag whose week it is!"
    send_message(msg)
    log('Sent {}'.format(msg))

sched.start()