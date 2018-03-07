from enigma.core.client import EnigmaClient, config, logger

# Client
bot = EnigmaClient()


def start():
    """
    Starts the bot and obtains all necessary config data.
    """
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )


@bot.event
async def on_ready():
    logger.info(f"Logged in as: {bot.user.name}, {bot.user.id}")
    await bot.change_presence()


if __name__ == "__main__":
    pass
