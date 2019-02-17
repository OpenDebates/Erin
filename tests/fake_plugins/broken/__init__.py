from tests.fake_plugins.broken.broken_extension import BrokenCommand


def setup(bot):
    bot.add_cog(BrokenCommand(bot))
