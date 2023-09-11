""""main.py"""
import uvicorn
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

@app.get("/", summary="API version", include_in_schema=False)
async def root():
    return {"message": "Canada lottery API", "version": "0.0.1"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)