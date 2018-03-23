CHECK_VANILLA_DB = \
"""
SELECT EXISTS (
   SELECT 1
   FROM   pg_tables 
   WHERE  schemaname = 'public'
   AND    tablename = 'guild'
);
"""

INITIALIZE_TABLES = \
"""
CREATE TABLE guild
(
  id INTEGER NOT NULL
    CONSTRAINT guild_pkey
    PRIMARY KEY
);

CREATE UNIQUE INDEX guild_id_uindex
  ON guild (id);

CREATE TABLE member
(
  id INTEGER NOT NULL
    CONSTRAINT member_pkey
    PRIMARY KEY
);

CREATE UNIQUE INDEX member_id_uindex
  ON member (id);

CREATE TABLE role
(
  id       INTEGER NOT NULL
    CONSTRAINT role_pkey
    PRIMARY KEY,
  guild_id INTEGER NOT NULL
    CONSTRAINT guild_id___fk
    REFERENCES guild
);

CREATE UNIQUE INDEX role_id_uindex
  ON role (id);

CREATE TABLE member_roles
(
  member_id INTEGER NOT NULL
    CONSTRAINT member_id___fk
    REFERENCES member,
  role_id   INTEGER NOT NULL
    CONSTRAINT role_id___fk
    REFERENCES role
);
"""