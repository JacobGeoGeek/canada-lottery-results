""""main.py"""
from fastapi import FastAPI
from .lottomax import lottomax_route

app = FastAPI()

app.include_router(lottomax_route.router)
