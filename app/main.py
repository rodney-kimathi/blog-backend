from fastapi import FastAPI

from app.config.database import create_database_engine
from app.config.settings import settings
from app.routes import access_routes, post_routes, root_routes

create_database_engine()

app = FastAPI(root_path=settings.root_path)

app.include_router(root_routes.router)
app.include_router(access_routes.router)
app.include_router(post_routes.router, prefix="/posts")
