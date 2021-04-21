# Package Info
import logging
import sys

from verboselogs import VerboseLogger

dist_name = "Erin"
__version__ = "0.1.0-alpha.1"

# Constants
LOG_FORMAT = "%(asctime)s %(name)-18s %(levelname)-8s %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S %z]"

# Set Library Logging Formats
logging.setLoggerClass(VerboseLogger)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
root_logger = logging.getLogger(__name__)
root_logger.addHandler(stream_handler)
