import logging

# Access Logger
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)


def get_hypercorn_logger(log_level: str) -> dict:
    log_level = log_level.upper()
    hypercorn_logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": f"{log_level}"},
        "loggers": {
            "hypercorn.error": {
                "level": f"{log_level}",
                "handlers": ["error_console"],
                "propagate": True,
                "qualname": "hypercorn.error",
            },
            "hypercorn.access": {
                "level": f"{log_level}",
                "handlers": ["console"],
                "propagate": True,
                "qualname": "hypercorn.access",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": "ext://sys.stdout",
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": "ext://sys.stderr",
            },
        },
        "formatters": {
            "generic": {
                "format": "%(asctime)s %(name)-18s %(levelname)-8s %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            }
        },
    }
    return hypercorn_logging_config
