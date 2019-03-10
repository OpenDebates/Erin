import logging

import discord
from discord.ext import commands

from glia.db.drivers import MongoClient
from glia.core.utils import find_plugins, get_plugin_data

# Logging
logger = logging.getLogger(__name__)


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
        self.logger = logger

        # Database
        if config['db'].get("enabled"):
            self.db = MongoClient(config, bot=self)
        else:
            self.logger.notice(
                "No db defined. Running without one!"
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
            logger.verbose(
                f"Plugins Found: {extensions}"
            )
        except Exception:
            self.logger.exception()
            self.logout()
            return None
        for extension in extensions:

            # Add schema validation as per DiscordFederation/Glia#12
            plugin_data = get_plugin_data(extension)
            if not plugin_data:
                self.logger.notice(
                    f"Skipping {extension}: `plugin_data` undefined"
                )
                continue

            # Convert to db method later
            if not self.config["db"].get("enabled"):
                if plugin_data.get("db"):
                    logger.notice(f"Skipping {extension}: Database Needed")
                    continue

            # Attempt loading the plugin
            try:
                self.logger.verbose(f"Loading Plugin: {extension}")
                self.load_extension(extension)
            except discord.ClientException:
                self.logger.exception(
                    f'Missing setup() for Plugin: {extension}.'
                )
            except ImportError:
                self.logger.exception(
                    f"Failed to load Plugin: {extension}"
                )
            except Exception as e:
                self.logger.exception("Core Error:")

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()

    async def on_command(self, ctx):
        if ctx.cog.__cog_name__:
            cog_name = ctx.cog.__cog_name__
        else:
            cog_name = repr(ctx.cog)

        self.logger.info(
            f"Cog: {cog_name} | "
            f"Invoked With: {ctx.invoked_with} | Message Content: \n"
            f"{ctx.message.content}"
        )
