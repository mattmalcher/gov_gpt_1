#!/bin/bash

# https://hub.docker.com/_/postgres
# https://medium.com/@beld_pro/quick-tip-creating-a-postgresql-container-with-default-user-and-password-8bb2adb82342
# https://www.postgresql.org/docs/current/sql-createschema.html
# https://medium.com/@prabhathsumindapathirana/getting-started-with-postgres-setting-up-a-user-schema-and-grants-bbb2a3f536df

set -e

# create a new user & db and give all privs to that user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $embed_user WITH PASSWORD '$embed_user_pw';
	CREATE DATABASE $embed_db_name;
	GRANT ALL PRIVILEGES ON DATABASE $embed_db_name TO $embed_user;    
EOSQL

# connect to new db as the new user and create a schema
psql -v ON_ERROR_STOP=1 --username "$embed_user" --dbname "$embed_db_name" <<-EOSQL
    CREATE SCHEMA $embed_schema_name;
EOSQL

# now create as the dba to the new db and add the extension 
# and set the new user to default to the new schema
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$embed_db_name" <<-EOSQL
    CREATE EXTENSION vector WITH SCHEMA $embed_schema_name;
	ALTER USER $embed_user SET search_path = $embed_schema_name, $embed_user, public; 
EOSQL