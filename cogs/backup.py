import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
from pymongo.errors import DuplicateKeyError

from documents import Customers, Message

logger = logging.getLogger()


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # sets the client variable so we can use it in cogs

    @commands.command()
    async def backup(self, ctx: Context):
        """Initial back up action."""
        # TODO: Make sure this can only happen exactly ONCE
        for channel in ctx.guild.channels:

            # Ignore non text channels
            if channel.type != discord.ChannelType.text:
                continue

            messages = await channel.history(limit=None, oldest_first=True).flatten()
            documents = []

            for message in messages:
                documents.append(
                    Message(
                        name=message.name,
                        content=message.content,
                        timestamp=message.created_at,
                    )
                )
            await Message.insert_many(documents)

    @commands.command(name="init")
    async def init_guild(self, ctx: Context):
        try:
            await Customers(
                name="Test",
                guild_id=ctx.guild.id,
                backup=False,
            ).insert()
            await ctx.send("Guild init.")
        except DuplicateKeyError:
            await ctx.send("Guild already in database.")


def setup(bot):
    bot.add_cog(Backup(bot))
