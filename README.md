# Canada Lottery API

## Overview
The Canada Lottery API is a code base that scrape the lottery results from external websites and send the data into JSON.

## Requirements
To use this API Project, you will need to install Python version 3.10 or later.

## Setup
After installing Python, you must
* Change the directory to canada-lottery-results `cd canada-lottery-results`
* Create a virtual environnement (e.g: `python -m venv \path\to\virtual\environnement`).
* Install the dependecies via the pip command: `pip install -r requirements.txt`.
* Start the api via uvicorn command: `uvicorn src.main:app`.


## Stack
This project use the following librares:
* [FastAPI](https://fastapi.tiangolo.com/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)