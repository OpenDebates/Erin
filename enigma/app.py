import logging

import coloredlogs
import toml

from enigma.core.client import EnigmaClient

# Client
bot = EnigmaClient()
config = toml.load("enigma/app.cfg")

# Logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


def start():
    """
    Starts the bot and obtains all necessary config data.
    """
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )


@bot.event
async def on_ready():
    logger.info(f"Logged in as: {bot.user.name}, {bot.user.id}")
    await bot.change_presence()


if __name__ == "__main__":
    pass
