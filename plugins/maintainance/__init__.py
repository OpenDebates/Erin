from plugins.maintainance.server_status import ServerStatus


def setup(bot):
    bot.add_cog(ServerStatus(bot))
