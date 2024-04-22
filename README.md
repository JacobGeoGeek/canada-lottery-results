# Canada Lottery API

## Overview
The Canada Lottery API is a code base that scrapes the lottery results from external websites and sends the data into JSON.

## Requirements
To use this API Project, you will need to install Python version 3.12 or later.

## Setup
After installing Python, you must
* Change the directory to canada-lottery-results `cd canada-lottery-results`
* Create a virtual environnement (e.g: `python -m venv \path\to\virtual\environnement`).
* Install the dependencies via the pip command: `pip install -r requirements.txt`.
* For the migrations, if you create a new migration script, you must run the following command: `alembic revision -m "SOME_TEXT_DESCRIPTION"`.
* To apply the migrations, you must run the following command: `alembic -x url=SOME_DATABASE_CONNECTION_STRING upgrade head`.
* To downgrade the migrations, you must run the following command: `alembic -x url=SOME_DATABASE_CONNECTION_STRING downgrade -1`.
* Start the API by typing the following command: `python WORK_FOLDER/src/main.py`.


## Environnement variables
* **ENVIRONNEMENT**: PROD or DEV. defeaut is `DEV`.
* **ROOT_PATH**: When the API is served via a proxy, the variable will add an extra path prefix that is not seen by your application. For more information: [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/?h=proxy). Default value: `""`,
* **PORT**: Specify the port that the API is running. Default value: `8080`.
* **HOST**: The IP address that the API is running. Default value: `0.0.0.0`.
* **RAPIDAPI_PROXY_SECRET**: The variable is used for production only. Its value from the RapidAPI platform checks if the incoming requests come from the RapidAPI only. Default value: `""`.
* **DATABASE_CONNECTION_STRING**: The DB connection string is used to connect to a Postgresql database. format of the string is `postgresql://USER_NAME:PASSWORD@HOST:PORT/DB_NAME`. Default value: `""`.
* **SENDER_EMAIL**: The email sender. The email will be used to send the lottery results to the recipient. Default value: `""`.
* **SENDER_PASSWORD**: The email sender's password. Default value: `""`.
* **RECIPIENT_EMAIL**: The email recipient. this email will receive the lottery results saved in the database. Default value: `""`.
* **SMTP_SERVER**: The SMTP server. Default value: `smtp.gmail.com`.
* **SMTP_PORT**: The SMTP port. Default value: `587`.


## Stack
This project uses the following libraries:
* [FastAPI](https://fastapi.tiangolo.com/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [alembic](https://alembic.sqlalchemy.org/en/latest/)
* [APScheduler](https://apscheduler.readthedocs.io/en/3.x/index.html)