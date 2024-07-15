from fastapi import FastAPI

from .routers import root_router

root_path = "/api/v1"

app = FastAPI(root_path=root_path)

app.include_router(root_router.router)
