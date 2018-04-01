import logging

from sanic import Sanic
from sanic.response import json

# Logging
from enigma.core.loggers import SANIC_LOGGER_CONFIG

logger = logging.getLogger(__name__)
web = Sanic(log_config=SANIC_LOGGER_CONFIG)


@web.route("/")
async def test(request):
    return json({"hello": "world"})
