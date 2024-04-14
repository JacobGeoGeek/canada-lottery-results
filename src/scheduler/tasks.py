import datetime
from src.celery_app import celery_app
from src.daily_grand.daily_grand_service import insert_new_daily_grand_result
from src.lottomax.lottomax_service import insert_new_lotto_result
from src.six_fourty_nine.six_fourty_nine_service import insert_new_649_result
from src.notification.email_sender import email_sender

@celery_app.task
def extract_lotto_max_results():
    print("Extracting lotto max results")
    insert_new_lotto_result(date=datetime.date(2024, 4, 12))

@celery_app.task
def extract_lotto_649_results():
    print("Extracting lotto 649 results")
    insert_new_649_result(date=datetime.date(2024, 4, 10))

@celery_app.task
def extract_daily_grand_results():
    print("Extracting Daily Grand results")
    insert_new_daily_grand_result(date=datetime.date(2024, 4, 11))