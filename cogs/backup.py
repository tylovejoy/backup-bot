import asyncio
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from documents import Customers, Message
from utils.database import create_msg_document

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

                documents.append(await create_msg_document(ctx.guild, message))
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
