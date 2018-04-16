from collections import deque

import discord
from discord.ext import commands

plugin_data = {
    "name": "Member Info"
}


class MemberInfo:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

        self.client = self.bot.db
        self.db = self.bot.db[self.bot.db.database]

    @commands.group(
        name="member", aliases=["memberinfo", "userinfo"],
        invoke_without_command=True
    )
    async def member(self, ctx, member: commands.MemberConverter):
        embed = discord.Embed(
            title=f'Member Info',
            url=f"https://unethical.me/wiki/{member.display_name}",
            timestamp=member.joined_at
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Joined server on")

        embed.add_field(name="Name", value=member.display_name, inline=True)
        rep = await self.client.get(member, 'reputation')
        if rep:
            embed.add_field(name="Reputation", value=f"{rep}", inline=True)

        aliases = await self.client.get(member, 'aliases')
        if aliases:
            embed.add_field(name="Aliases", value=", ".join(aliases))
        await ctx.send(embed=embed)

    @member.group(name="add")
    async def add(self, ctx):
        pass

    @add.command(name="alias")
    async def add_alias(self, ctx, alias: commands.clean_content):
        if len(alias) > 32:
            embed = discord.Embed(
                color=0x7F8C8D,
                title="❌ Aliases must be less than 32 characters in length! ❌"
            )
            await ctx.send(embed=embed)
            return
        aliases = await self.client.get(ctx.author, 'aliases')
        if aliases is not None:
            if len(aliases) < 3:
                await self.client.upsert(ctx.author, aliases=aliases+[alias])
            else:
                aliases = deque(aliases)
                aliases.popleft()
                await self.client.upsert(
                    ctx.author, aliases=list(aliases)+[alias]
                )
        else:
            await self.client.upsert(ctx.author, aliases=[alias])

        response = discord.Embed(
            color=0x7F8C8D,
            title="✅ Alias added! ✅"
        )
        await ctx.send(embed=response)


def setup(bot):
    bot.add_cog(MemberInfo(bot))
