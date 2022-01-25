import logging
import pathlib
from datetime import datetime
from os import environ
from typing import List, Optional

import motor
from beanie import Document, Indexed, init_beanie
from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger()


class Message(Document):
    """Model for messages."""

    name: str
    message_id: int
    content: str
    timestamp: datetime
    channel_id: int
    attachments: Optional[List[Optional[pathlib.Path]]]


class Channels(Document):
    """Model for channels."""

    name: str
    category_name: str
    channel_id: int


class Customers(Document):
    """Model for customers."""

    guild_id: Indexed(int, unique=True)
    name: str
    backup: bool
