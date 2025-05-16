from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo
from .entities.user import User
from .api import register_routes

from .logging import configure_logging, LogLevels

configure_logging(LogLevels.info)


app = FastAPI()

"""
Only uncomment below to create new tables,
otherwise the tets will fail if not connected
"""
# Base.metedata.create_all(bind=engine)

register_routes(app)