import re
from typing import Dict

import asyncpg

from enigma.core.exceptions import EnigmaDatabaseError
from .queries import CHECK_VANILLA_DB, INITIALIZE_TABLES


class EnigmaDatabase:
    def __init__(self, bot, config, logger):
        # Internal
        self.conn = None
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
        self.conn = await asyncpg.connect(self.uri)
        await self._startup()

    async def disconnect(self):
        await self.conn.close()
        self._logger.info("Disconnecting from the database")

    async def _startup(self):
        records = await self.conn.fetch(CHECK_VANILLA_DB)

        if records[0]['exists']:
            self._logger.info("Previous configs found in database")
        else:
            self._logger.info("Populating database")
            async with self.conn.transaction():
                await self.conn.execute(INITIALIZE_TABLES)

    async def set(self, ctx, key: str, value: str):
        guild_id = ctx.guild.id
        row = await self.conn.fetchrow(
            "SELECT * FROM public.guild WHERE id = $1 AND key = $2",
            str(guild_id),
            str(key)
        )
        if row is None:
            await self.conn.execute(
                "INSERT into public.guild VALUES ($1, $2, $3)",
                str(guild_id),
                str(key),
                str(value)
            )
        else:
            await self.conn.execute(
                """
                UPDATE public.guild
                SET value = $1 WHERE key = $2 and id = $3
                """,
                str(value),
                str(key),
                str(guild_id)
            )

    async def get(self, ctx, key: str):
        guild_id = ctx.guild.id
        row = await self.conn.fetchrow(
            "SELECT * FROM public.guild WHERE id = $1 AND key = $2",
            str(guild_id),
            str(key)
        )
        if row is None:
            return row
        else:
            return row['value']

    async def upsert(self, table: str, **columns: Dict[str, int or str]):
        """
        This is used to `upsert` column values to a table  which means
        to insert a row if it is not found or update it if it already
        exists with the new values.

        :param table: table name in string format
        :param columns: column-to-value mapping as params
        """

        # Check if table has a primary key
        row = await self.conn.fetchrow(
            """
            SELECT *
            FROM information_schema.table_constraints
            WHERE constraint_type = 'PRIMARY KEY'
            AND table_name = $1;
            """,
            table
        )
        if row is None:
            raise EnigmaDatabaseError(f"Table {table} has no primary key.")
        row = await self.conn.fetchrow(
            """
            SELECT count(*) FROM information_schema.columns
            WHERE table_name = $1
            """,
            table
        )
        if row[0] == len(columns):
            query_repr = list(map(lambda x: repr(x), list(columns.values())))

            # Check if a record exists
            conditions = ""
            for key, value in columns.items():
                conditions += f"{key} = {repr(value)} AND "
            conditions = re.sub('\sAND\s$', '', conditions)
            select_query = \
                f"""
                SELECT * FROM public.{table}
                WHERE {conditions}
                """
            record = await self.conn.fetchrow(select_query)

            if record is None:
                # Insert record
                values = ", ".join(query_repr)
                insert_query = f"INSERT into public.{table} VALUES ({values})"
                await self.conn.execute(insert_query)
            else:
                # Update record
                set_values = ""
                for key, value in columns.items():
                    set_values += f"{key} = {repr(value)}, "
                set_values = re.sub(',\s$', '', set_values)
                update_query = \
                    f"""
                    UPDATE public.{table} SET {set_values} 
                    WHERE {conditions}
                    """
                await self.conn.execute(update_query)
        else:
            raise EnigmaDatabaseError(f"Table needs {row[0]} columns passed.")
