import datetime

from discord.ext import commands

plugin_data = {
    "name": "Server Status"
}


class ServerStatus:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

    @commands.command(name="ping")
    async def ping(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - ctx.message.created_at
        await ctx.send(f"Pong: {delta}ms")


def setup(bot):
    bot.add_cog(ServerStatus(bot))

