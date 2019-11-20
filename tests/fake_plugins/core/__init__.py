from tests.fake_plugins.core.error import CommandError
from tests.fake_plugins.core.navigation import HelpMenu
from tests.fake_plugins.core.startup import Login

plugin_data = {"name": "Test Core Plugins"}


def setup(bot):
    bot.add_cog(CommandError(bot))
    bot.add_cog(HelpMenu(bot))
    bot.add_cog(Login(bot))
