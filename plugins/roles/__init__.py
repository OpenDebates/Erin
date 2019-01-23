from plugins.roles.role_persist import PersistRoles


def setup(bot):
    bot.add_cog(PersistRoles(bot))
