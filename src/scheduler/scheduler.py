from celery import Celery
from celery.schedules import crontab

class Scheduler:
  def __init__(self,broker_url: str, result_backend: str) -> None:
    self._app: Celery = Celery(__name__, broker=broker_url, backend=f"db+{result_backend}", include=['src.scheduler.tasks'])
    self._app.conf.beat_schedule = {
      'extract_lotto_max_results': {
        'task': 'src.scheduler.tasks.extract_lotto_max_results',
        'schedule': crontab(hour=5, minute=30, day_of_week='tuesday,friday')
      },
      'extract_lotto_649_results': {
        'task': 'src.scheduler.tasks.extract_lotto_649_results',
        'schedule': crontab(hour=5, minute=30, day_of_week='wednesday,saturday')
      },
      'extract_daily_grand_results': {
        'task': 'src.scheduler.tasks.extract_daily_grand_results',
        'schedule': crontab(hour=5, minute=30, day_of_week='monday,thursday')
      },
    }

    self._app.conf.update(timezome='America/Toronto', enable_utc=True)

  def get_celey_app(self) -> Celery:
    return self._app