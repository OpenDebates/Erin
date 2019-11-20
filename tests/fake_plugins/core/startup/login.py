import discord
from discord.ext import commands


class Login(commands.Cog, name="Login"):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        self.bot.logger.info(f"Logged in as: {self.bot.user.name}, {self.bot.user.id}")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="over Discord"
            )
        )


def setup(bot):
    bot.add_cog(Login(bot))
