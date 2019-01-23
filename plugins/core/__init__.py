from plugins.core.error import CommandError
from plugins.core.navigation import Help
from plugins.core.startup import Login


def setup(bot):
    bot.add_cog(CommandError(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Login(bot))
