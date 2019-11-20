import discord
from discord.ext import commands


class CommandError(commands.Cog, name="Command Error"):
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, exception):

        if isinstance(exception, commands.NoPrivateMessage):
            response = discord.Embed(
                title="⛔ Access denied. This is a server only command.", color=0xBE1931
            )
            return await ctx.author.send(embed=response)

        self.bot.logger.exception(f"ERROR: {exception}", exc_info=exception)


def setup(bot):
    bot.add_cog(CommandError(bot))
