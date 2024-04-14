
from celery import Celery

from src.config.configuration import configuration
from src.scheduler.scheduler import Scheduler

celery_app: Celery = Scheduler(configuration.broker_url, configuration.database_connection_string).get_celey_app()

if __name__ == "__main__":
    celery_app.start()