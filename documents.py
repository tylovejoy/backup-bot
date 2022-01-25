from typing import List

import motor
from beanie import Document, init_beanie
from datetime import datetime


class Message(Document):
    name: int
    content: str
    timestamp: datetime
    channel_name: str
    attachment: List[str]


class Channels(Document):
    name: str
    category_name: str


async def init():
    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://user:pass@host:27017"
    )

    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=Document.__subclasses__())
