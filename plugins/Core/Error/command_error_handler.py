import discord
from discord.ext import commands

plugin_data = {
    "name": "Command Error"
}


class CommandError:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

    async def on_command_error(self, ctx, exception):
        try:
            plugin_name = ctx.cog.data['name']
        except AttributeError as e:
            plugin_name = None

        if plugin_name:
            self.bot.logger.plugin(
                f"{plugin_name}"
                f"{[ctx.invoked_with]}: {ctx.message.content}\n"
                f"ERROR: {exception}"
            )

        else:
            self.bot.logger.command(
                f"{ctx.invoked_with}: {ctx.message.content}\n"
                f"ERROR: {exception}"
            )

        if isinstance(exception, commands.NoPrivateMessage):
            response = discord.Embed(
                title='⛔ Access denied. This is a server only command.',
                color=0xBE1931
            )
            return await ctx.author.send(embed=response)


def setup(bot):
    bot.add_cog(CommandError(bot))
