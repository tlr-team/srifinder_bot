import logging

from .handlers import bot

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_bot():
    # Start the Bot
    bot.polling()

