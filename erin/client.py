import logging

import discord
from discord.ext import commands

import plugins
from erin.core.database import MongoClient
from erin.core.utils import find_plugins, get_plugin_data

# Logging
logger = logging.getLogger('erin')


class ErinClient(commands.Bot):
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

        # Logger
        self.logger = logger

        # Database
        if config['database'].get("enabled"):
            self.db = MongoClient(config, bot=self)
        else:
            self.logger.warning("No database defined. Running without one!")

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
        try:
            extensions = find_plugins(plugins)
            logger.debug(
                f"Plugins: {extensions}"
            )
        except Exception as e:
            logger.exception()
            self.logout()
            return None
        for extension in extensions:

            # Add schema validation as per DiscordFederation/Erin#12
            plugin_data = get_plugin_data(extension)
            if not plugin_data:
                continue

            # Convert to db method later
            if not self.config["database"].get("enabled"):
                if plugin_data.get("database"):
                    self.logger.info(f"Skipping {extension}: Database Needed")
                    continue

            # Attempt loading the plugin
            try:
                logger.plugin(f"Loading Plugin: {extension}")
                self.load_extension(extension)
            except discord.ClientException as e:
                logger.exception(
                    f'Missing setup() for Plugin: {extension}.'
                )
            except ImportError as e:
                logger.exception(
                    f"Failed to load Plugin: {extension}"
                )
            except Exception as e:
                logger.exception("Core Error")

    def add_cog(self, cog):
        super().add_cog(cog)

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()

    async def on_command(self, ctx):
        try:
            cog_name = ctx.cog.data['name']
        except AttributeError as e:
            cog_name = None

        if cog_name:
            logger.command(
                f"Cog: {cog_name} | "
                f"Invoked With: {ctx.invoked_with} | Message Content: \n"
                f"{ctx.message.content}"
            )
        else:
            pass
