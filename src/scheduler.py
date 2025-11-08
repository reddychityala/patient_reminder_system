from apscheduler.schedulers.blocking import BlockingScheduler
from etl_pipeline import run_etl

scheduler = BlockingScheduler()

# Run every 1 minute for testing
@scheduler.scheduled_job('interval', minutes=1)
def scheduled_etl():
    run_etl()

print("🕒 Scheduler started — ETL will run every 1 minute (for testing).")
scheduler.start()

from notification_utils import send_email_alert
send_email_alert("ETL Success", "ETL ran successfully.", "you@example.com")

