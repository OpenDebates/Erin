from discord.ext import commands


class SchemaCommand(commands.Cog, name="Schema Command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="schema")
    async def broken(self, ctx):
        await ctx.send("Sorry, I'm a broken schema!")


def setup(bot):
    bot.add_cog(SchemaCommand(bot))
