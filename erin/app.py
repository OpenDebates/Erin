import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

import toml

import erin
from erin.client import ErinClient
from erin.core.loggers import access_logger
from erin.core.schema import ENV_MAPPINGS, OPTIONAL_ENVS, config_schema
from erin.core.utils import config_loader

logger = logging.getLogger(__name__)
root_logger = logger.parent

# Set Discord Logging Formats
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)

# Global Bot Variable
bot = None


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    if kwargs["log_level"]:
        # Set logger level
        level = logging.getLevelName(kwargs["log_level"].upper())
        root_logger.setLevel(level)
    else:
        root_logger.setLevel("INFO")
    # Config Loader
    try:
        if kwargs["config_file"]:
            config = toml.load(kwargs["config_file"])
        else:
            config = toml.load("erin/erin.toml")
    except FileNotFoundError:
        logger.notice(
            "No config file provided. " "Checking for environment variables instead."
        )
        config = config_loader(ENV_MAPPINGS, OPTIONAL_ENVS)

    # Override configs from config file with ones from cli
    if kwargs["log_level"]:
        config["bot"]["log_level"] = kwargs["log_level"].upper()

    # Validate Config
    config_schema.validate(config)

    logger.info(f"Starting Erin: {erin.__version__}")

    # Discord Debug Logging
    if config["bot"].get("debug"):
        discord_logger.setLevel(logging.DEBUG)

    discord_handler = RotatingFileHandler(
        filename=".logs/discord.log",
        encoding="utf-8",
        mode="a",
        maxBytes=10 ** 7,
        backupCount=5,
    )

    access_handler = RotatingFileHandler(
        filename=".logs/access.log",
        encoding="utf-8",
        mode="a",
        maxBytes=10 ** 7,
        backupCount=5,
    )

    if config["bot"].get("log_type") == "Timed":
        discord_handler = TimedRotatingFileHandler(
            filename=".logs/discord.log",
            when="midnight",
            interval=1,
            backupCount=5,
            encoding="utf-8",
        )

    discord_logger.addHandler(discord_handler)
    access_logger.addHandler(access_handler)

    # Faster Event Loop
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

    # Initialize Bot
    global bot
    bot = ErinClient(config)
    bot.remove_command("help")
    bot.setup()

    try:
        bot.run(config["bot"]["token"], bot=True, reconnect=True)
    except (KeyboardInterrupt, SystemExit):
        bot.close()
    finally:
        sys.exit()


if __name__ == "__main__":
    start()
