import logging

import discord
from discord.ext import commands

from glia.core.database import MongoClient
from glia.core.utils import find_plugins, get_plugin_data

# Logging
glia_logger = logging.getLogger('glia')
plugin_logger = logging.getLogger('plugin')
command_logger = logging.getLogger('command')
database_logger = logging.getLogger('database')


class GliaClient(commands.Bot):
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
        self.logger = plugin_logger

        # Database
        if config['database'].get("enabled"):
            self.db = MongoClient(config, bot=self)
        else:
            database_logger.warning(
                "No database defined. Running without one!"
            )

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
        plugin_dir = self.config["bot"].get("plugins_folder")
        try:
            extensions = find_plugins(plugin_dir)
            glia_logger.debug(
                f"Plugins Found: {extensions}"
            )
        except Exception:
            glia_logger.exception()
            self.logout()
            return None
        for extension in extensions:

            # Add schema validation as per DiscordFederation/Glia#12
            plugin_data = get_plugin_data(extension)
            if not plugin_data:
                glia_logger.warning(
                    f"Skipping {extension}: `plugin_data` undefined"
                )
                continue

            # Convert to db method later
            if not self.config["database"].get("enabled"):
                if plugin_data.get("database"):
                    glia_logger.info(f"Skipping {extension}: Database Needed")
                    continue

            # Attempt loading the plugin
            try:
                glia_logger.debug(f"Loading Plugin: {extension}")
                self.load_extension(extension)
            except discord.ClientException:
                glia_logger.exception(
                    f'Missing setup() for Plugin: {extension}.'
                )
            except ImportError:
                glia_logger.exception(
                    f"Failed to load Plugin: {extension}"
                )
            except Exception:
                glia_logger.exception("Core Error")

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()

    async def on_command(self, ctx):
        try:
            cog_name = ctx.cog.data['name']
        except AttributeError:
            cog_name = None

        if cog_name:
            command_logger.info(
                f"Cog: {cog_name} | "
                f"Invoked With: {ctx.invoked_with} | Message Content: \n"
                f"{ctx.message.content}"
            )
        else:
            pass
