import enigma

from enigma.core.client import config, EnigmaClient, logger


def start():
    """
    Starts the bot and obtains all necessary config data.
    """
    logger.info(f"Starting Enigma: {enigma.__version__}")
    bot = EnigmaClient()
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )
