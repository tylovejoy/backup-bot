import logging
from os import environ

import discord
from discord.ext import commands

from bot import BackupBot
from documents import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandle = logging.StreamHandler()
consoleHandle.setLevel(logging.INFO)
consoleHandle.setFormatter(
    logging.Formatter("%(name)-18s :: %(levelname)-8s :: %(message)s")
)
logger.addHandler(consoleHandle)

bot = BackupBot()


@bot.command()
async def backup(ctx: discord.ext.commands.Context):
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


TOKEN = environ["TOKEN"]
bot.run(TOKEN)
