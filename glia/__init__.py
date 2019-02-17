# -*- coding: utf-8 -*-

from glia.core.loggers import setup_custom_logger

# Package Info
dist_name = 'Glia'
__version__ = "0.1.0.dev0"

# Logging Formats
logger = setup_custom_logger('glia')
plugin_logger = setup_custom_logger('plugin')
command_logger = setup_custom_logger('command')
database_logger = setup_custom_logger('database')

