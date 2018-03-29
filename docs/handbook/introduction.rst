.. _dev_intro:

.. _discord.py: https://github.com/Rapptz/discord.py/tree/rewrite

============
Introduction
============

Building a discord bot can sometimes be overwhelming if you need complex commands. Keeping track of logging,
configuration files, databases, efficiency, sharding, devops and more. With Enigma you don't have to worry
about the boring parts and focus on building your commands the way you need them.

Prerequisite Knowledge
======================

Simple Commands
----------------------------

- You must have built a very basic bot using discord.py_
- Basic experience with :mod:`asyncio`

Advanced Commands
------------------------------

- Experience using relational databases
- Knowledge of SQL (not mandatory unless want to access the database directly)

Terminology
===========

Before we begin building commands, there's some jargon you need to get familiar with.

**Cogs:**

Quoting `add_cog <http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.ext.commands.Bot.add_cog>`_ in the discord.py_ documentation.

    "A cog is a class that has its own event listeners and commands.

    They are meant as a way to organize multiple relevant commands into a singular class that shares some state or no state at all."

**Extensions:**

From the discord.py_ docs

    "An extension is a python module that contains commands, cogs, or listeners."

**Plugins:**

Plugins are simply extensions that have cogs with extra metadata and custom methods called in it. An existing cog can be converted into a plugin by defining a ``plugin_data`` variable in it's class.
However, plugins are not guaranteed to work as a cog in another discord bot.

**Plugin Metadata:**

This is simply a local ``plugin_data`` variable of type :obj:`dict` defined in a plugin. This defines metadata like the name, description, status and other properties of a plugin.

**Plugin Setup:**

This is a local ``setup()`` function defined outside the cog's class. It's used to do initialize cogs and prepare the plugin to be imported as an extension.
Although it is fairly easy to initialize other cogs and commands directly from the `setup()` function, it's recommended to only place commands that complement each other into the same plugin.
