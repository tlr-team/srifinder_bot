import logging

from json import load
from os.path import isfile
from .handlers import bot

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_bot():
    # Start the Bot
    bot.polling()

