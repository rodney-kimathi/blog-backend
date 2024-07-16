from fastapi import FastAPI

from app.routes import root_routes

root_path = "/api/v1"

app = FastAPI(root_path=root_path)

app.include_router(root_routes.router)
