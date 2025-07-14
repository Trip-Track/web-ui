#!/usr/bin/env bash
set -euo pipefail


STOPS_CSV=${STOPS_CSV:-/csv/stops.csv}
CONNS_CSV=${CONNS_CSV:-/csv/connections.csv}

PGHOST=${PGHOST:-db}
PGUSER=${PGUSER:-trips}
PGDATABASE=${PGDATABASE:-trips}
: "${PGPASSWORD:?PGPASSWORD/DB_PASSWORD must be set}"


echo "Waiting for Postgres …"
until pg_isready -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" >/dev/null 2>&1; do
  sleep 1
done
echo "Database ready – REPLACING data from CSV"

psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" <<SQL

TRUNCATE TABLE connections, stops RESTART IDENTITY CASCADE;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TEMP TABLE _stops_raw (
  code text,
  name text,
  lat  double precision,
  lon  double precision
);

\copy _stops_raw(code,name,lat,lon) FROM '${STOPS_CSV}' WITH (FORMAT csv, HEADER);

INSERT INTO stops(id, code, name, lat, lon)
SELECT gen_random_uuid(), code, name, lat, lon
FROM _stops_raw;

CREATE TEMP TABLE _conns_raw (
  from_code text,
  to_code   text,
  weight    double precision
);

\copy _conns_raw(from_code,to_code,weight) FROM '${CONNS_CSV}' WITH (FORMAT csv, HEADER);

INSERT INTO connections(id, from_id, to_id, weight)
SELECT gen_random_uuid(),
       s_from.id,
       s_to.id,
       r.weight
FROM _conns_raw r
JOIN stops s_from ON s_from.code = r.from_code
JOIN stops s_to   ON s_to.code   = r.to_code;
SQL

echo "CSV import complete – database now contains fresh data."
