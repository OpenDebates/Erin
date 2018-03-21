========================
Basic Usage Instructions
========================

Configuring Enigma
==================

To start using Enigma, we to get some configuration details.
First let's make sure Enigma is installed.

::

    $ enigma -V
    enigma 0.1.0.dev

Looks good! So, we need to head over to the `discord developers portal <https://discordapp.com/developers/applications/me/create>`_ and create our bot user.

.. figure:: ../_static/images/create_app_discord.png
    :alt: Create a discord app

Now this is the most important part. We need to create a configuration file which is also valid TOML.

.. code-block:: cfg

    [bot]

    token = ""

    [database]

    host = ""
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
Save your changes and use this link replacing ``BOT_CLIENT_ID`` with your bot's client ID to invite Enigma to our server,

Invite Link : ``https://discordapp.com/api/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=8&scope=bot``

You can get the client ID from your bot's app page.

.. figure:: ../_static/images/get_client_id.png
    :alt: Client ID

Now that we have all the details, we can start filling in our config file. It should look something like this.
You should also already have your database connection details. If not, read `Configuring a database <../installation/database>`_.

.. code-block:: cfg

    [bot]

    token = "NDI2MTE3OTg5MTA1MTM5NzEy.DZRbXQ.CYHYtqRXjWYgJO9PqLoIv-HT8SE"

    [database]

    host = "myvps.com" # This can also be an IP address
    port = 5432
    username = "pingbot"
    password = "ilov3bacon"
    database = "pingbot"

    [global]

    prefixes = ["!" , "="]
    description = "I will ping you back. Don't worry!"

