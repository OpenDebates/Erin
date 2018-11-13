# -*- coding: utf-8 -*-
import logging

from enigma.core.loggers import BotLogger

dist_name = 'Enigma'
__version__ = "0.1.0.dev0"

# Set Custom Global Logger
# This needs to be above all other code.
logging.setLoggerClass(BotLogger)

# Logging Formats
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S %z]"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
