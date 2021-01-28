====
Tags
====

Prerequisites
=============

- You will need a MongoDB client like Robo3T or Compass to view collections
- An IDE or code editor like Pycharm, Atom, Sublime etc
- Minimal knowledge of collections, documents, databases and CRUD operations in MongoDB

Guide
=====

Tags are commands used to save frequently sent messages like rules, instructions and help information in a guild.
It's a very useful feature and implemented in a lot of bots on discord. So let's build one for our self.

Before we begin building our plugin, we need an idea of what our command will look like. We want users to be
able to use newlines and any characters without sacrificing usability.

It will look something like this for a user in a guild:

.. code-block:: text

   +tag add rules

   __**Chat Rules**__
   **1.** An important rule
   **2.** Another rule

   __**Voice Chat Rules**__
   **1.** Don't scream in voice chat
   **2.** No trolling


Now that we know what we want our command to look like, let's create our plugin.
Create a ``tags.py`` file in the ``Plugins/`` directory and put this code in it.
You can remove the comments if you want.

.. code-block:: python3

   import discord
   from discord.ext import commands

   plugin_data = {
       "name": "Tags",
       "database": True
   }

   class Tag(commands.Cog, name="Tag"):
       def __init__(self, bot):
           self.bot = bot
           self.data = plugin_data

           # Easier access to common variables
           self.logger = self.bot.logger

       @commands.command(
           name="tag"
       )
       @commands.guild_only()  # Only allow usage from inside a guild
       async def tag(self, ctx, tag: str):
           """
           This will take a single parameter tag when someone uses the
           command +tag my_tag. Here my_tag will get passed to tag and
           ultimately to our logger.
           """
           self.logger.debug(f"Tag: {tag})


Now :ref:`start erin <starting_erin>` and send a test command with a tag name to ensure everything works properly.
If everything went smoothly, we need to figure out to how to store data so it can be retrieved later.
Not to worry, erin has made it very easy to store data without worrying about relational data too much.

We need to use a driver to talk to our database. Don't worry, Erin takes care of this for you. But you will need to be aware that we are using it
to do operations on the database.

- `Motor Documentation <https://motor.readthedocs.io/en/stable/>`_
- `PyMongo Documentation <https://pymongo.readthedocs.io/en/stable/>`_

Let's begin by adding an ``add`` sub command to our existing command to allow adding new tags.
In order to do this, we need to use a feature of the `discord.py <https://discordpy.readthedocs.io/en/latest/>`_ library called Groups.
You can learn more about groups `here <https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-subcommand>`_.

.. code-block:: python3

   class Tag(commands.Cog, name="Tag"):
       def __init__(self, bot):
           self.bot = bot
           self.data = plugin_data

           # self.bot.db.database is simply the name of the database
           # you provided in the app's config file.
           # self.db is a Database object much similar to what's found in
           # PyMongo. Except, here we are using the asynchronous version
           # of the library called Motor.
           self.db = self.bot.db[self.bot.db.database]
           self.logger = self.bot.logger

       # Notice this is now group()
       # Setting invoke_without_command=True makes sure sub commands don't
       # run the code in this function when they are called.
       @commands.group(
           name="tag",
           invoke_without_command=True
       )
       @commands.guild_only()
       async def tag(self, ctx, tag: str):
           document = await self.db.tags.find_one({"tag": tag})
           self.logger.debug(f"Tag: {tag} | Document: {document}")

       # Notice that we are using the tag coroutine as a decorator here.
       @tag.command(name="add")
       async def add_tag(self, ctx, tag: str, *, content: commands.clean_content):
            """
            Notice the '*' used after the tag param. This will ensure that
            the content of the message after the tag won't get passed into
            our coroutine. In short, without the '*', it will raise an
            error for more than one argument after the tag.

            With the '*' it will consider everything after the tag as a
            string with newlines and spaces intact. commands.clean_content
            also makes sure the input is more clean and will do some
            parsing for you.
            """

            # Let's insert our first document into the collection.
            # MongoDB is lazy when creating collections. It is a convention
            # to name collections after the cog or the extension to make it
            # easier to locate. Here this line will create a tags
            # collection as well as insert the json file as a document.
            self.db.tags.insert_one(
                {"guild_id": ctx.guild.id, "tag": tag, "content": content}
            )

Run ``+tag add mytag 123`` or something similar (preferably with newlines and spaces as well) from discord to ensure
there are no errors. Then check you MongoDB client to make sure that the document's were inserted.

If all went well we can add some code to display the tags.

.. code-block:: python3

   @commands.group(
           name="tag",
           invoke_without_command=True
       )
       @commands.guild_only()
       async def tag(self, ctx, tag: str):
           # Find the document with the tag that we inserted earlier
           document = await self.db.tags.find_one({"tag": tag})
           self.logger.debug(f"Tag: {tag} | Document: {document}")
           if document:
               # Send a message to the guild with the content
               await ctx.send(document["content"])
           else:
               # These are embeds that make thinks look prettier. Here we
               # made a simple error message.
               response = discord.Embed(
                   color=0x7F8C8D,
                   title="❌ Tag does not exist! ❌"
               )
               await ctx.send(embed=response)

       @tag.command(name="add")
       async def add_tag(self, ctx, tag: str, *, content: commands.clean_content):
           # Let's check to make sure the tag doesn't already exist.
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

That wasn't too hard was it? Let's add some more commands and functionality to make a full blown plugin.
You can see the full code here.

.. code-block:: python3

   import discord
   from discord.ext import commands

   plugin_data = {
       "name": "Tags",
       "database": True
   }


   class Tag(commands.Cog, name="Tag"):
       def __init__(self, bot):
           self.bot = bot
           self.data = plugin_data

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

Congratulations! You reached the end of this tutorial. You should now have sufficient knowledge to make more kinds of
plugins.
