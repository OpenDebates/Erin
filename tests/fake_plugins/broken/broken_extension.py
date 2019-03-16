from discord.ext import commands


class BrokenCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {
            "name": "Broken Command"
        }

    @commands.command(name="broken")
    async def broken(self, ctx):
        await ctx.send("Sorry, I'm broken!")


def setup(bot):
    bot.add_cog(BrokenCommand(bot))
