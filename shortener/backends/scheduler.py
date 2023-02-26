from apscheduler.schedulers.background import BackgroundScheduler
from .delete_expired_urls import delete_expired_urls


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        delete_expired_urls,
        "interval",
        days=1,
        id="delete_expired_urls_001",
        replace_existing=True,
    )

    scheduler.start()
