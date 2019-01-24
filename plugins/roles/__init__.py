from plugins.roles.role_persist import PersistRoles

plugin_data = {
    "name": "Erin Role Plugins",
    "database": "mongodb"
}


def setup(bot):
    bot.add_cog(PersistRoles(bot))
