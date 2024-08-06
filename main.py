# api_gateway/app/main.py

from fastapi import FastAPI
from app.api.v1.endpoints import user, auth, auth_service, vehicle

app = FastAPI()

app.include_router(gateway.router, prefix="/api/v1", tags=["gateway"])
app.include_router(vehicle.router, prefix="/api/v1", tags=["vehicle"])
app.include_router(auth_service.router, prefix="/api/v1", tags=["auth_service"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


@app.get("/")
def read_root():
    return {"Hello": "API Gateway"}
