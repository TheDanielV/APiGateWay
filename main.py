# api_gateway/app/main.py

from fastapi import FastAPI
from app.api.v1.endpoint import gateway

app = FastAPI()

app.include_router(gateway.router, prefix="/api/v1", tags=["gateway"])


@app.get("/")
def read_root():
    return {"Hello": "API Gateway"}
