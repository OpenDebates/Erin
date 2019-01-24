from plugins.utilities.tags import Tag

plugin_data = {
    "name": "Erin Utility Plugins",
    "database": "mongodb"
}


def setup(bot):
    bot.add_cog(Tag(bot))
