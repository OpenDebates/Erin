import logging
import traceback

import plugins
from discord.ext import commands
from enigma.core.utils import find_cogs

logger = logging.getLogger("enigma.app")


class EnigmaClient(commands.Bot):
    """
    Custom implementation designed to load configuration from the TOML
    config file and dynamic console configurations
    """
    def __init__(self):
        super().__init__(
            command_prefix=self._get_command_prefix(),
            description=self._get_description()
        )

    def _get_command_prefix(self):
        self.prefixes = [">"]
        return self.prefixes[0]

    def _get_description(self):
        self.description = "Polyglot Discord Bot"
        return self.description

    def _load_plugins(self):
        for extension in find_cogs(plugins):
            try:
                self.load_extension(extension)
            except Exception as e:
                logger.error(
                    f'Failed to load extension {extension}.'
                )
                traceback.print_exc()

    def setup(self):
        """
        Important setup functions and their configurations have to be
        called here.
        """
        self._load_plugins()
