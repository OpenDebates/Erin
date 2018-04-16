import discord
from discord.ext import commands

plugin_data = {
    "name": "Reputation"
}


class Reputation:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

        self.client = self.bot.db
        self.db = self.bot.db[self.bot.db.database]

    @commands.group(
        name="reputation", aliases=["rep"], invoke_without_command=True
    )
    @commands.guild_only()
    async def reputation(self, ctx):
        pass

    @reputation.command(name="populate")
    async def populate(self, ctx):
        response = discord.Embed(
            color=0x696969,
            title=f'🔍 Processing {ctx.message.guild.member_count} members.'
        )
        await ctx.send(embed=response)
        for member in ctx.guild.members:
            rep = await self.client.get(member, 'reputation')
            if rep is None:
                await self.client.upsert(member, reputation=1000)

    async def on_member_join(self, member):
        rep = await self.client.get(member, 'reputation')
        if rep is None:
            await self.client.upsert(member, reputation=1000)


def setup(bot):
    bot.add_cog(Reputation(bot))
