from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from server.models.users import *
from server.routers import basic, users

app = FastAPI()

app.include_router(basic.router)
app.include_router(users.router)


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["server.models.users"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
