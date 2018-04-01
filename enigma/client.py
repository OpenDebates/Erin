import logging

import discord
from discord.ext import commands

import plugins
from enigma.core.database import MongoClient
from enigma.core.loggers import BotLogger
from enigma.core.utils import find_cogs, get_plugin_data

# Logging
logger = BotLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S %z]"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class EnigmaClient(commands.Bot):
    """
    Custom implementation designed to load configuration from the TOML
    config file and dynamic console configurations
    """
    def __init__(self, config, *args, **kwargs):
        self.config = config

        super().__init__(
            command_prefix=self._get_command_prefix(),
            description=self._get_description(),
            *args, **kwargs
        )

        # Database
        self.db = MongoClient(config, logger, bot=self)

        # Logger
        self.logger = logger

    def _get_command_prefix(self):
        self.prefixes = self.config["global"]["prefixes"]
        return self.prefixes

    def _get_description(self):
        self.description = self.config["global"]["description"]
        if self.description:
            return self.description
        else:
            return ""

    def _load_plugins(self):
        for extension in find_cogs(plugins):
            try:
                plugin_data = get_plugin_data(extension)
                logger.info(f"Loading Plugin: {plugin_data['name']}")
                self.load_extension(extension)
            except discord.ClientException as e:
                logger.exception(
                    f'Missing setup() for plugin: {extension}.'
                )
            except ImportError as e:
                logger.exception(
                    f"Failed to load plugin: {extension}"
                )
            except Exception as e:
                logger.exception("Core Error")

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()

    async def on_command(self, ctx):
        try:
            plugin_name = ctx.cog.data['name']
        except AttributeError as e:
            plugin_name = None

        if plugin_name:
            logger.plugin(
                f"{plugin_name}"
                f" [{ctx.invoked_with}]: {ctx.message.content}"
            )
        else:
            logger.command(
                f"{ctx.invoked_with}: {ctx.message.content}"
            )
