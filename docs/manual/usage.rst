.. _basic_usage:

========================
Basic Usage Instructions
========================

Configuring Erin
==================

To start using Erin, we to get some configuration details.
First let's make sure Erin is installed.

::

    $ erin -V
    erin 0.1.0.dev

Looks good! So, we need to head over to the `discord developers portal <https://discordapp.com/developers/applications/me/create>`_ and create our bot user.

.. figure:: ../_static/images/create_app_discord.png
    :alt: Create a discord app

Now this is the most important part. We need to create a configuration file which is also valid TOML.

.. code-block:: ini

    [bot]

    token = ""

    [database]

    host = []
    port =
    username = ""
    password = ""
    database = ""

    [global]

    prefixes = []
    description = ""

To fill this out we need to know some details about our discord bot user. Simply scrolling down and clicking "Create a Bot User" will do the job.

.. figure:: ../_static/images/create_bot_user.png
    :alt: Create a Bot User

Next click to reveal the token.

.. figure:: ../_static/images/click_to_reveal.png
    :alt: Click to reveal token

    Make sure to copy this token down!

For now we won't be delving in making our bot public and we'll stick to using our bot privately in a server of our choice.
Save your changes and use this link replacing ``BOT_CLIENT_ID`` with your bot's client ID to invite Erin to our server,

Invite Link : ``https://discordapp.com/api/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=8&scope=bot``

You can get the client ID from your bot's app page.

.. figure:: ../_static/images/get_client_id.png
    :alt: Client ID

Now that we have all the details, we can start filling in our config file. It should look something like this.
You should also already have your database connection details. If not, read :ref:`configuring_database`.

.. code-block:: cfg

    [bot]

    token = "NDI2MTE3OTg5MTA1MTM5NzEy.DZRbXQ.CYHYtqRXjWYgJO9PqLoIv-HT8SE"

    [database]

    host = ["myvps.com"] # This can also be a list of hosts (including replica sets)
    port = 27017
    username = "pingbot"
    password = "ilov3bacon"
    database = "pingbot"
    replica_set = "rs0"  # This is needed added when using replica sets

    [global]

    prefixes = ["+" , ">"]
    description = "I will ping you back. Don't worry!"

.. _starting_erin:

Starting Erin
===============

Now that we have a config file ready. Let's save it is somewhere. By convention, it's named ``config.toml``.

Now let's tell Erin to start by passing the path to this file as an argument.

::

    erin start --config /path/to/config.toml


.. note::

    You can also save it as ``Erin/erin/erin.toml`` in the repository if you installed from source.
    However, you must make sure to name it ``erin.toml`` in this case or Erin will switch to trying environment variables.
