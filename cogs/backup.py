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

    async def _backup_messages(self, ctx: Context):
        """Back up all messages.z"""

        await Message.init_model(
            AsyncIOMotorDatabase(self.bot.client, str(ctx.guild.id)), False
        )

        for channel in ctx.guild.channels:

            # Ignore non text channels
            if channel.type != discord.ChannelType.text:
                continue

            messages = await channel.history(limit=None, oldest_first=True).flatten()
            documents = []

            for message in messages:
                file_paths = []
                if message.attachments:
                    for i, attachment in enumerate(message.attachments):
                        original = attachment.filename.split(".")
                        file_name = f"files/{ctx.guild.id}/{message.channel.id}/{message.id}_{original[0]}_{i}.{original[1]}"
                        file_paths.append(file_name)
                        os.makedirs(os.path.dirname(file_name), exist_ok=True)
                        await attachment.save(file_name)

                logger.info(file_paths)
                d = Message(
                    name=message.author.name,
                    content=message.content,
                    timestamp=message.created_at,
                    message_id=message.id,
                    channel_id=message.channel.id,
                    attachment=file_paths,
                )
                documents.append(d)
            if documents:
                await Message.insert_many(documents)

    @commands.command(name="init")
    async def init_guild(self, ctx: Context):
        """Initialize backup of guild."""
        try:
            await Customers(
                name="Test",
                guild_id=ctx.guild.id,
                backup=False,
            ).insert()

        except DuplicateKeyError:
            await ctx.send("Guild already in database.")
            return

        await self._backup_messages(ctx)
        await ctx.send("Guild init.")


def setup(bot):
    bot.add_cog(Backup(bot))
