import logging
from typing import Sequence

import discord
from discord import RawMessageDeleteEvent, RawMessageUpdateEvent
from discord.abc import GuildChannel
from discord.ext.commands import Bot

from documents import Message, database_init

logger = logging.getLogger()
intents = discord.Intents(
    guilds=True,
    emojis=True,
    messages=True,
)

description = "Back up and restore your entire server."


class BackupBot(Bot):
    def __init__(self):
        super().__init__(intents=intents, description=description, command_prefix="?")

    @staticmethod
    async def on_connect():
        """Connection to Discord event."""
        await database_init()

    async def on_ready(self):
        """Bot is ready event."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})\n\n")

    async def on_message(self, message: discord.Message):
        """Back up new messages."""
        # await Message(
        #     name=message.name,
        #     content=message.content,
        #     timestamp=message.created_at,
        # ).insert()
        await self.process_commands(message)

    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        """Remove deleted messages from the database."""

    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent):
        """Edit messages in the database."""

    async def on_guild_channel_create(self, channel: GuildChannel):
        """Add new guild channels."""

    async def on_guild_channel_delete(self, channel: GuildChannel):
        """Remove guild channels."""

    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        """Edit channels."""

    async def on_guild_role_create(self, role: discord.Role):
        """Add new role."""

    async def on_guild_role_delete(self, role: discord.Role):
        """Remove role."""

    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        """Edit role."""

    async def on_guild_emojis_update(
        self,
        guild: discord.Guild,
        before: Sequence[discord.Emoji],
        after: Sequence[discord.Emoji],
    ):
        """Update emojis."""
