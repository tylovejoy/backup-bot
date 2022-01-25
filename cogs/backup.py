import asyncio
import errno
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import Context
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from documents import Customers, Message

logger = logging.getLogger()


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # sets the client variable so we can use it in cogs

    async def _backup_messages(self, ctx: Context, info_msg: discord.Message):
        """Back up all messages."""

        await Message.init_model(
            AsyncIOMotorDatabase(self.bot.client, str(ctx.guild.id)), False
        )

        for i_channel, channel in enumerate(ctx.guild.channels):

            # Ignore non text channels
            if channel.type != discord.ChannelType.text:
                continue

            messages = await channel.history(limit=None, oldest_first=True).flatten()
            documents = []

            if not messages:
                await asyncio.sleep(1)  # help rate limiting
                await info_msg.edit(
                    content=f"{i_channel} / {len(ctx.guild.channels)} channels."
                )

            for i_message, message in enumerate(messages):
                if i_message % 100 == 0:
                    await asyncio.sleep(1)  # help rate limiting
                    await info_msg.edit(
                        content=(
                            f"{i_channel} / {len(ctx.guild.channels)} channels.\n"
                            f"{i_message} / {len(messages)} messages."
                        )
                    )

                file_paths = []
                if message.attachments:
                    for i, attachment in enumerate(message.attachments):
                        original = attachment.filename.split(".")
                        file_name = f"files/{ctx.guild.id}/{message.channel.id}/{message.id}_{original[0]}_{i}.{original[1]}"
                        file_paths.append(file_name)
                        os.makedirs(os.path.dirname(file_name), exist_ok=True)
                        await attachment.save(file_name)

                documents.append(
                    Message(
                        name=message.author.name,
                        content=message.content,
                        timestamp=message.created_at,
                        message_id=message.id,
                        channel_id=message.channel.id,
                        attachments=file_paths if file_paths else None,
                    )
                )
            if documents:
                await Message.insert_many(documents)

    @commands.command(name="init")
    async def init_guild(self, ctx: Context):
        """Initialize backup of guild."""
        info_msg = await ctx.send("Hello, I will start backing up your server now!")

        try:
            await Customers(
                name="Test",
                guild_id=ctx.guild.id,
                backup=False,
            ).insert()

        except DuplicateKeyError:
            await info_msg.edit(content="Guild already in database.")
            return

        await self._backup_messages(ctx, info_msg)
        await info_msg.edit(content="Guild has been initialized.")


def setup(bot):
    bot.add_cog(Backup(bot))
