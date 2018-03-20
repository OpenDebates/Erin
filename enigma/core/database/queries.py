CHECK_VANILLA_DB = \
"""
   SELECT EXISTS (
       SELECT 1
       FROM   pg_tables 
       WHERE  schemaname = 'public'
       AND    tablename = 'guild_config'
   );
"""

INITIALIZE_TABLES = \
"""
    CREATE TABLE guild_config
    (
      guild_id INTEGER NOT NULL
        CONSTRAINT guild_config_pkey
        PRIMARY KEY,
      owner_id INTEGER NOT NULL
    );
    
    CREATE UNIQUE INDEX guild_config_guild_id_uindex
      ON guild_config (guild_id);
    
    CREATE UNIQUE INDEX guild_config_owner_id_uindex
      ON guild_config (owner_id);
"""