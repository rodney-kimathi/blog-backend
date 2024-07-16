from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from app.config.database import create_database_engine
from app.routes import access_routes, root_routes

root_path = "/api/v1"
app = FastAPI(root_path=root_path)


@app.on_event("startup")
def on_startup() -> None:
    load_dotenv(find_dotenv())
    create_database_engine()


app.include_router(root_routes.router)
app.include_router(access_routes.router)
