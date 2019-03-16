from discord.ext import commands


class BrokenCommand(commands.Cog, name="Broken Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="broken")
    async def broken(self, ctx):
        await ctx.send("Sorry, I'm broken!")


def setup(bot):
    bot.add_cog(BrokenCommand(bot))
