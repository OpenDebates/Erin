import asyncio
import logging

import toml

import erin
from erin.client import ErinClient
from erin.core.constants import ENV_MAPPINGS, OPTIONAL_ENVS
from erin.core.loggers import discord_logger
from erin.core.utils import config_loader

logger = logging.getLogger('erin')


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    if kwargs['log_level']:
        # Set app level
        level = logging.getLevelName(kwargs['log_level'].upper())
        logger.setLevel(level)
    else:
        logger.setLevel('INFO')
    logger.info(f"Starting Erin: {erin.__version__}")

    # Config Loader
    try:
        if kwargs['config_file']:
            config = toml.load(kwargs['config_file'])
        else:
            config = toml.load("erin/erin.toml")
    except FileNotFoundError as e:
        logger.info(
            "No config file provided. "
            "Checking for environment variables instead."
        )
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
    bot = ErinClient(config)
    bot.remove_command("help")
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )


if __name__ == "__main__":
    start()
