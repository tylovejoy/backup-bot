import logging
import os
from os import environ
from typing import Sequence

import discord
import motor
from beanie import init_beanie
from discord import RawMessageDeleteEvent, RawMessageUpdateEvent
from discord.abc import GuildChannel
from discord.ext.commands import Bot
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from documents import Customers, Message
from utils.database import create_msg_document

logger = logging.getLogger()
intents = discord.Intents(
    guilds=True,
    emojis=True,
    messages=True,
)

description = "Back up and restore your entire server."


DB_PASSWORD = environ["DB_PASSWORD"]


class BackupBot(Bot):
    def __init__(self):
        super().__init__(intents=intents, description=description, command_prefix="?")
        self.client = None

    async def database_init(self):
        """Initialze MongoDB connection."""
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb+srv://backup-bot:{DB_PASSWORD}@mapbot.oult0.mongodb.net/customers?retryWrites=true&w=majority"
        )

        try:
            await init_beanie(
                database=self.client.customers, document_models=[Customers]
            )
        except ServerSelectionTimeoutError:
            logger.critical("Connecting database - FAILED!!!")

        else:
            logger.info("Connecting database - SUCCESS!")

    async def on_connect(self):
        """Connection to Discord event."""
        await self.database_init()

    async def on_ready(self):
        """Bot is ready event."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})\n\n")

    async def on_message(self, message: discord.Message):
        """Back up new messages."""
        await self.process_commands(message)
        await Message.init_model(
            AsyncIOMotorDatabase(self.client, str(message.guild.id)), False
        )
        await (await create_msg_document(message.guild, message)).insert()

    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        """Remove deleted messages from the database."""
        await Message.init_model(
            AsyncIOMotorDatabase(self.client, str(payload.guild_id)), False
        )
        message = await Message.find_one(Message.message_id == payload.message_id)
        if message:
            await message.delete()

    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent):
        """Edit messages in the database."""
        await Message.init_model(
            AsyncIOMotorDatabase(self.client, str(payload.guild_id)), False
        )
        message = await Message.find_one(Message.message_id == payload.message_id)
        if not message:
            return

        data = payload.data
        # TODO: this is duplicated code.
        file_paths = []
        if data["attachments"]:
            for i, attachment in enumerate(data["attachments"]):
                original = attachment["filename"].split(".")
                file_name = (
                    f"files/{payload.guild_id}/{payload.channel_id}/"
                    f"{payload.message_id}_{original[0]}_{i}.{original[1]}"
                )
                file_paths.append(file_name)
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                await attachment.save(file_name)
        message.content = data["content"]
        message.attachments = file_paths if file_paths else None
        await message.save()

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
