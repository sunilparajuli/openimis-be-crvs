from django.apps import AppConfig
from .utils.mediator import register_mediator, send_heartbeat
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
MODULE_NAME = 'crvs'

DEFAULT_CFG = {
}

class openIMISopenCRVSConfig(AppConfig):
    name = MODULE_NAME

    def ready(self):
        register_mediator()
        scheduler = BackgroundScheduler()
        interval_seconds = settings.OPENHIM_CONFIG.get('heartbeat_interval', 100)  # Default to 10 seconds if not set

        # Schedule the heartbeat function
        scheduler.add_job(send_heartbeat, 'interval', seconds=interval_seconds)
        scheduler.start()        

