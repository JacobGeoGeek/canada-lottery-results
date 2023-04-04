""""main.py"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .lottomax import lottomax_route


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lottomax_route.router)
