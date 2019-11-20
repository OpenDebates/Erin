from tests.fake_plugins.schema.schema_extension import SchemaCommand

plugin_data = {"name": "Schema Plugin", "database": "enabled"}


def setup(bot):
    bot.add_cog(SchemaCommand(bot))
