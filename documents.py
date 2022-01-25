import logging
import pathlib
from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed

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
