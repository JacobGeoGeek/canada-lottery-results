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


## Environnement variables
* **ENVIRONNEMENT**: PROD or DEV. defeaut is `DEV`.
* **ROOT_PATH**: When the API is served via a proxy, the variable will add an extra path prefix that is not seen by your application. For more information: [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/?h=proxy). Default is `""`
* **PORT**: Specify the port that the API is running. Default is `8080`.
* **HOST**: The IP adresse that the API is running. Default is `0.0.0.0`
* **RAPIDAPI_PROXY_SECRET**: The variable is used for production only. Its value from the RapidAPI platform that checks if the incoming requests come from the RapidAPI only. Default is `""`.

## Stack
This project use the following librares:
* [FastAPI](https://fastapi.tiangolo.com/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)