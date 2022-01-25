import logging
import os
from os import environ

from bot import BackupBot

logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandle = logging.StreamHandler()
consoleHandle.setLevel(logging.INFO)
consoleHandle.setFormatter(
    logging.Formatter("%(name)-18s :: %(levelname)-8s :: %(message)s")
)
logger.addHandler(consoleHandle)

bot = BackupBot()

for f in os.listdir("./cogs"):
    if f.endswith(".py"):
        bot.load_extension("cogs." + f[:-3])

TOKEN = environ["TOKEN"]
bot.run(TOKEN)
