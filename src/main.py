from fastapi import FastAPI
from .database.core import engine, Base
from .entities.todo import Todo
from .entities.user import User
from .api import register_routes
from random import randint
import copy
from opentelemetry import trace

tracer = trace.get_tracer("clean-architecture-fastapi-server.tracer")

from .logging import configure_logging, LogLevels

configure_logging(LogLevels.info)


app = FastAPI()

"""
Only uncomment below to create new tables,
otherwise the tets will fail if not connected
"""
# Base.metedata.create_all(bind=engine)

register_routes(app)


dice_roll = [[], [], []]


@app.get("/rolldice")
async def roll_dice():
    count = 0

    # Roll dice and distribute results into three separate lists
    while count < 15:
        if count < 5:
            dice_roll[0].append(roll())  # Append to the first list
        elif count < 10:
            dice_roll[1].append(roll())  # Append to the second list
        else:
            dice_roll[2].append(roll())  # Append to the third list
        count += 1

    # Store the result to return
    result = copy.deepcopy(dice_roll)

    # Clear the dice_roll lists for the next function cal After returning the result
    dice_roll[0].clear()
    dice_roll[1].clear()
    dice_roll[2].clear()

    # Return the result
    return {"dice_rolls": result}

def roll():
    with tracer.start_as_current_span("clean_architecture") as clean_architecture_span:
        result =  randint(1, 6)
        clean_architecture_span.set_attribute("clean_architecture.value", result)
        return result
