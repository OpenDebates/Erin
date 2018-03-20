import asyncpg

from .queries import CHECK_VANILLA_DB, INITIALIZE_TABLES


class EnigmaDatabase:
    def __init__(self, bot, config, logger):
        # Internal
        self._conn = None
        self._logger = logger

        # Config
        self.host = config["database"]["host"]
        self.port = config["database"]["port"]
        self.database = config["database"]["database"]
        self.username = config["database"]["username"]
        self.password = config["database"]["password"]
        self.uri = f"postgresql://{self.username}:{self.password}" \
                   f"@{self.host}/{self.database}"

    async def connect(self):
        self._logger.info(
            f"Connecting to database {self.database} at {self.host}"
        )
        self._conn = await asyncpg.connect(self.uri)

    async def disconnect(self):
        await self._conn.close()
        self._logger.info("Disconnecting from the database")

    async def _startup(self):
        records = await self._conn.fetch(CHECK_VANILLA_DB)

        if records[0]['exists']:
            self._logger.info("Previous configs found in database")
        else:
            self._logger.info("Populating database")
            await self._conn.execute(INITIALIZE_TABLES)
