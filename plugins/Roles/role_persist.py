from discord.ext import commands

plugin_data = {
    "name": "Role Persist"
}


class RolePersist:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

    @commands.group(
        name="rolepersist",
        shorthelp="Saves the roles of a member.",
        aliases=["persistrole", "rp", "pr"]
    )
    @commands.guild_only()
    async def role_persist(self, ctx):
        pass

    @role_persist.command(
        name="global",
        shorthelp="Toggle persistent roles for all member."
    )
    async def toggle_global(self, ctx):
        pass


def setup(bot):
    bot.add_cog(RolePersist(bot))
