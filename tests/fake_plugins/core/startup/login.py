import discord


class Login:
    def __init__(self, bot):
        self.bot = bot
        self.data = {
            "name": "Login"
        }

    async def on_ready(self):
        self.bot.logger.info(
            f"Logged in as: {self.bot.user.name}, {self.bot.user.id}"
        )
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="over Discord"
            )
        )


def setup(bot):
    bot.add_cog(Login(bot))
