import asyncio
import logging

import toml

import enigma
from enigma.client import EnigmaClient, logger
from enigma.core.constants import ENV_MAPPINGS, OPTIONAL_ENVS
from enigma.core.loggers import discord_logger
from enigma.core.utils import config_loader


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    if kwargs['log_level']:
        # Set app level
        level = logging.getLevelName(kwargs['log_level'].upper())
        logger.setLevel(level)
    logger.info(f"Starting Enigma: {enigma.__version__}")

    # Config Loader
    try:
        if kwargs['config_file']:
            config = toml.load(kwargs['config_file'])
        else:
            config = toml.load("enigma/app.cfg")
    except FileNotFoundError as e:
        logger.warning("Looks like enigma/app.cfg is missing.")
        logger.info("Checking for environment variables instead.")
        config = config_loader(ENV_MAPPINGS, OPTIONAL_ENVS)

    # Discord Debug Logging
    try:
        if config["bot"]["debug"]:
            discord_logger.setLevel(logging.DEBUG)
    except KeyError:
        pass

    # Faster Event Loop
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

    # Initialize Bot
    bot = EnigmaClient(config)
    bot.remove_command("help")
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )


if __name__ == "__main__":
    start()
