import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
from server.models.users import *
from server.routers import basic, users, auth

load_dotenv()
app = FastAPI(
    title=os.getenv("APP_TITLE"),
    description=os.getenv("APP_DESCRIPTION"),
    version=os.getenv("APP_VERSION"),
    debug=bool(os.getenv("APP_DEBUG")),
    include_in_schema=bool(os.getenv("APP_SCHEMA"))
)

app.include_router(basic.router)
app.include_router(users.router)
app.include_router(auth.router)

register_tortoise(
    app,
    db_url=os.getenv("DB_URL"),
    modules={"models": ["server.models.users", "server.models.clients"]},
    generate_schemas=bool(os.getenv("DB_SCHEMAS")),
    add_exception_handlers=bool(os.getenv("DB_EXCEPTION_HANDLERS")),
)
