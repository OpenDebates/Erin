from discord.ext import commands

from enigma.utils import find_members

plugin_data = {
    "name": "Persist Roles"
}


class PersistRoles:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

    @commands.group(
        name="persistroles",
        shorthelp="Saves the roles of a member.",
        aliases=["pr"],
        invoke_without_command=True
    )
    @commands.guild_only()
    async def persist_roles(self, ctx):
        members = find_members(ctx)
        for member in members:
            await self.save_roles(member)

    async def save_roles(self, member):
        print(f"Roles for {member} saved.")

    @persist_roles.command(
        name="global",
        shorthelp="Toggle persistent roles for all members."
    )
    async def toggle_global(self, ctx):
        toggled = await self.bot.db.get(ctx, "persistrole_global")
        if toggled is None or toggled == "False":
            await self.bot.db.set(ctx, "persistrole_global", "True")
        else:
            await self.bot.db.set(ctx, "persistrole_global", "False")

    async def on_member_join(self, member):
        print(f"{member.guild}: {member.id}")


def setup(bot):
    bot.add_cog(PersistRoles(bot))
