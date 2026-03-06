from apscheduler.schedulers.background import BackgroundScheduler
from services.monitoring_service import check_devices

scheduler = BackgroundScheduler()

def start_scheduler():

    scheduler.add_job(
        check_devices,
        'interval',
        seconds=10
    )

    scheduler.start()