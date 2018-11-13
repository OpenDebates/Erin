import discord
from discord.ext import commands


class Tag:
    def __init__(self, bot):
        self.bot = bot
        self.data = {
            "name": "Tags"
        }

        # Easier Access
        self.db = self.bot.db[self.bot.db.database]
        self.logger = self.bot.logger

    @commands.group(
        name="tag",
        invoke_without_command=True
    )
    @commands.guild_only()
    async def tag(self, ctx, tag: str):
        document = await self.db.tags.find_one({"tag": tag})
        self.logger.debug(f"Tag: {tag} | Document: {document}")
        if document:
            await ctx.send(document["content"])
        else:
            response = discord.Embed(
                color=0x7F8C8D,
                title="❌ Tag does not exist! ❌"
            )
            await ctx.send(embed=response)

    @tag.command(name="add")
    async def add_tag(self, ctx, tag: str, *, content: commands.clean_content):
        document = await self.db.tags.find_one({"tag": tag})
        if document:
            response = discord.Embed(
                color=0x7F8C8D,
                title="❌ Tag already exists! ❌"
            )
            await ctx.send(embed=response)
        else:
            self.db.tags.insert_one(
                {"guild_id": ctx.guild.id, "tag": tag, "content": content}
            )

    @tag.group(
        name="delete",
        invoke_without_command=True
    )
    async def delete_tag(self, ctx, tag: str):
        document = await self.db.tags.find_one({"tag": tag})
        if document:
            await self.db.tags.delete_one({"tag": tag})
        else:
            response = discord.Embed(
                color=0x7F8C8D,
                title="❌ Tag not found! ❌"
            )
            await ctx.send(embed=response)

    @tag.command(name="list")
    async def list_tags(self, ctx):
        tags = []
        async for document in self.db.tags.find({"guild_id": ctx.guild.id}):
            tags.append(document["tag"])
        if len(tags) > 0:
            await ctx.send("\n".join(tags))
        else:
            response = discord.Embed(
                color=0x7F8C8D,
                title="❌ No tags to list! ❌"
            )
            await ctx.send(embed=response)

    @delete_tag.command(name="all")
    async def delete_all_tags(self, ctx):
        await self.db.tags.delete_many({"guild_id": ctx.guild.id})
        response = discord.Embed(
            color=0x7F8C8D,
            title="✅ All tags deleted! ✅"
        )
        await ctx.send(embed=response)


def setup(bot):
    bot.add_cog(Tag(bot))
