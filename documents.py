import logging
from datetime import datetime
from os import environ
from typing import List

import motor
from beanie import Document, Indexed, init_beanie
from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger()


class Message(Document):
    """Model for messages."""

    name: int
    content: str
    timestamp: datetime
    channel_name: str
    attachment: List[str]


class Channels(Document):
    """Model for channels."""

    name: str
    category_name: str


class Customers(Document):
    """Model for customers."""

    guild_id: Indexed(int, unique=True)
    name: str
    backup: bool


DB_PASSWORD = environ["DB_PASSWORD"]


async def database_init():
    """Initialze MongoDB connection."""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb+srv://mapbot:{DB_PASSWORD}@mapbot.oult0.mongodb.net/doombot?retryWrites=true&w=majority"
    )

    try:
        await init_beanie(database=client.customers, document_models=[Customers])
    except ServerSelectionTimeoutError:
        logger.critical("Connecting database - FAILED!!!")

    else:
        logger.info("Connecting database - SUCCESS!")
