import logging
import pathlib
from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel

logger = logging.getLogger()


class Thread(BaseModel):
    """Model for a Thread."""

    thread_id: int
    name: str
    locked: bool
    archived: bool


class Message(Document):
    """Model for messages."""

    name: str
    message_id: int
    content: str
    timestamp: datetime
    channel_id: int
    attachments: Optional[List[Optional[pathlib.Path]]]
    thread: Optional[Thread]


class ChannelCategoryChildren(BaseModel):
    """Model for list of category children."""

    stage_channels: List[Optional[str]] = []
    text_channels: List[Optional[str]] = []
    voice_channels: List[Optional[str]] = []


class Channel(Document):
    """Model for channels."""

    name: str
    channel_id: int
    position: int
    channel_type: str
    slowmode_delay: int = 0
    topic: Optional[str]
    nsfw: Optional[bool]
    permissions_synced: Optional[bool]
    children: Optional[ChannelCategoryChildren]


class Customers(Document):
    """Model for customers."""

    guild_id: Indexed(int, unique=True)
    name: str
    backup: bool
