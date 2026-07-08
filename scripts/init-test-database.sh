#!/bin/sh
set -eu

: "${TEST_DB_NAME:?TEST_DB_NAME is required}"
: "${TEST_DB_USER:?TEST_DB_USER is required}"
: "${TEST_DB_PASSWORD:?TEST_DB_PASSWORD is required}"

echo "Ensuring PostgreSQL test role '$TEST_DB_USER' and database '$TEST_DB_NAME' exist"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set test_db="$TEST_DB_NAME" \
    --set test_user="$TEST_DB_USER" \
    --set test_password="$TEST_DB_PASSWORD" <<'SQL'
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'test_user', :'test_password')
WHERE NOT EXISTS (
    SELECT FROM pg_roles WHERE rolname = :'test_user'
)\gexec

SELECT format('CREATE DATABASE %I OWNER %I', :'test_db', :'test_user')
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = :'test_db'
)\gexec
SQL
