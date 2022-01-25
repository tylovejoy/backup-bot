import discord
from discord.ext import commands

from documents import Message

intents = discord.Intents.all()
intents.presences = False

bot = commands.Bot(command_prefix='?', description="", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    await Message(
        name=message.name,
        content=message.content,
        timestamp=message.created_at,
    ).insert()


@bot.command()
async def backup(ctx: discord.ext.commands.Context):
    for channel in ctx.guild.channels:
        print(channel.name, channel.id)
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


bot.run('ODc4ODgyMzY0NjExMjYwNDU2.YSHo_A.30V4Et8fURCjBDOjTzZ4-7Pxj7w')


