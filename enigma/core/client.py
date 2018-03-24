import traceback

import coloredlogs
import discord
from discord.ext import commands

import plugins
from enigma.core.database import EnigmaDatabase
from enigma.core.loggers import EnigmaLogger, LEVEL_STYLES
from enigma.core.utils import find_cogs, get_plugin_data

# Logging
logger = EnigmaLogger(__name__)
coloredlogs.install(
    level='INFO',
    logger=logger,
    level_styles=LEVEL_STYLES,
    fmt="%(asctime)s %(hostname)s pid:%(process)d %(levelname)s %(message)s"
)


class EnigmaClient(commands.Bot):
    """
    Custom implementation designed to load configuration from the TOML
    config file and dynamic console configurations
    """
    def __init__(self, config):
        self.config = config

        super().__init__(
            command_prefix=self._get_command_prefix(),
            description=self._get_description()
        )

        # Database
        self.db = EnigmaDatabase(self, config, logger)

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
                logger.plugin(f"Loading: {plugin_data['name']}")
                self.load_extension(extension)
            except discord.ClientException as e:
                logger.error(
                    f'Missing setup() for plugin: {extension}.'
                )
                traceback.print_exc()
            except ImportError as e:
                logger.error(
                    f"Failed to load plugin: {extension}"
                )
                traceback.print_exc()

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()

    async def on_ready(self):
        logger.info(f"Logged in as: {self.user.name}, {self.user.id}")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="over Unethical"
            )
        )

        await self.db.connect()
        await self.db._startup()
