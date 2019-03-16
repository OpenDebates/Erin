from discord.ext import commands


class SchemaCommand():
    def __init__(self, bot):
        self.bot = bot
        self.data = {
            "name": "Schema Command"
        }

    @commands.command(name="schema")
    async def broken(self, ctx):
        await ctx.send("Sorry, I'm a broken schema!")


def setup(bot):
    bot.add_cog(SchemaCommand(bot))
