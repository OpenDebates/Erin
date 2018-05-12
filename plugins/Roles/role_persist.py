import discord
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
        response = discord.Embed(
            color=0x77B255, title='✅ All roles are now persistent.'
        )
        await ctx.send(embed=response)

    async def save_roles(self, member):
        role_ids = [role.id for role in member.roles]
        await self.bot.db.upsert(member, roles=role_ids)

    @persist_roles.command(
        name="guild",
        shorthelp="Toggle persistent roles for all members."
    )
    async def toggle_guild(self, ctx):
        toggled = await self.bot.db.get(ctx.guild, "persistrole_guild")
        if toggled is None or toggled == "False":
            await self.bot.db.upsert(
                ctx.guild, persistrole_global=True
            )
            response = discord.Embed(
                color=0x696969,
                title=f'🔍 Processing {ctx.message.guild.member_count} members.'
            )
            await ctx.send(embed=response)

            for member in ctx.guild.members:
                await self.save_roles(member)

            response = discord.Embed(
                color=0x77B255, title='✅ All roles are now persistent.'
            )
            await ctx.send(embed=response)

        else:
            await self.bot.db.set(
                ctx.guild, persistrole_global=False
            )

    async def on_member_join(self, member):
        persist_enabled = await self.bot.db.get(
            member.guild, 'persistrole_guild'
        )
        if persist_enabled is not True:
            return
        all_role_ids = await self.bot.db.get(member, 'roles')
        if all_role_ids and len(all_role_ids) > 1:
            for persist_role in all_role_ids[1:]:
                role = discord.utils.find(lambda x: x.id == persist_role,
                                          member.guild.roles)
                await member.add_roles(role)

    async def on_member_update(self, before, after):
        persist_enabled = await self.bot.db.get(
            after.guild, 'persistrole_guild'
        )
        if persist_enabled and before.roles != after.roles:
            role_ids = [role.id for role in after.roles]
            await self.bot.db.upsert(after, roles=role_ids)


def setup(bot):
    bot.add_cog(PersistRoles(bot))
