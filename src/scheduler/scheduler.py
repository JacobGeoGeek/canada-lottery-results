import datetime
from typing import Final
from apscheduler.schedulers.background import BackgroundScheduler

from src.daily_grand.daily_grand_service import insert_new_daily_grand_result
from src.lottomax.lottomax_service import insert_new_lotto_result
from src.six_fourty_nine.six_fourty_nine_service import insert_new_649_result

class Scheduler:
  def __init__(self) -> None:
    self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'America/Toronto'})

    self.scheduler.add_job(self._insert_latest_lotto_max_result, 'cron', id="lotto_max", day_of_week='wed,sat', hour=5, minute=30)
    self.scheduler.add_job(self._insert_latest_649_result, 'cron', id="6_49", day_of_week='thu,sun', hour=5, minute=30)
    self.scheduler.add_job(self._insert_latest_daily_grand_result, 'cron', id="daily_grand", day_of_week='tue,fri', hour=5, minute=30)

  def _insert_latest_lotto_max_result(self):
    date_yesterday: Final[datetime.date] = datetime.date.today() - datetime.timedelta(days=1)
    print(f"insert latest lotto max result {date_yesterday}")
    insert_new_lotto_result(date_yesterday)
  
  def _insert_latest_649_result(self):
    date_yesterday: Final[datetime.date] = datetime.date.today() - datetime.timedelta(days=1)
    print(f"insert latest 649 result {date_yesterday}")
    insert_new_649_result(date_yesterday)

  def _insert_latest_daily_grand_result(self):
    date_yesterday: Final[datetime.date] = datetime.date.today() - datetime.timedelta(days=1)
    print(f"insert latest daily grand result {date_yesterday}")
    insert_new_daily_grand_result(date_yesterday)
  
  def start(self):
    self.scheduler.start()
  
  def stop(self):
    self.scheduler.shutdown()