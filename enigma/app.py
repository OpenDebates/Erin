import toml

import enigma
from enigma.core.client import EnigmaClient, logger
from enigma.core.constants import ENV_MAPPINGS, OPTIONAL_ENVS
from enigma.core.utils import config_loader


def start(*config_file):
    """
    Starts the bot and obtains all necessary config data.
    """
    logger.info(f"Starting Enigma: {enigma.__version__}")

    # Config Loader
    try:
        if config_file:
            config = toml.load(config_file[0].name)
        else:
            config = toml.load("enigma/app.cfg")
    except FileNotFoundError as e:
        logger.warning("Looks like enigma/app.cfg is missing.")
        logger.info("Checking for environment variables instead.")
        config = config_loader(ENV_MAPPINGS, OPTIONAL_ENVS)

    bot = EnigmaClient(config)
    bot.setup()
    bot.run(
        config['bot']['token'],
        bot=True,
        reconnect=True
    )


if __name__ == "__main__":
    start()
