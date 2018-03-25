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
  id    VARCHAR NOT NULL,
  key   VARCHAR,
  value VARCHAR
);

CREATE TABLE member
(
  id VARCHAR NOT NULL
    CONSTRAINT member_pkey
    PRIMARY KEY
);

CREATE UNIQUE INDEX member_id_uindex
  ON member (id);

CREATE TABLE role
(
  id VARCHAR NOT NULL
    CONSTRAINT role_pkey
    PRIMARY KEY
);

CREATE UNIQUE INDEX role_id_uindex
  ON role (id);

CREATE TABLE member_roles
(
  member_id VARCHAR
    CONSTRAINT member_id__fk
    REFERENCES member,
  role_id   VARCHAR
    CONSTRAINT role_id__fk
    REFERENCES role
);
"""