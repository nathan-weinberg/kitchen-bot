from apscheduler.schedulers.blocking import BlockingScheduler
from app import send_message

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon', hour=23)
def kitchen_reminder():
    msg = "This is a test kitchen reminder! Soon I will tag whose week it is!"
    send_message(msg)

sched.start()