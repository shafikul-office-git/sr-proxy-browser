from fastapi import FastAPI
from . import users, browser

def register_routers(app: FastAPI):
    app.include_router(users.router)
    app.include_router(browser.router) 