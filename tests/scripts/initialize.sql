BEGIN;
CREATE SCHEMA IF NOT EXISTS "celsus_contacts" AUTHORIZATION postgres;
SET search_path TO celsus_contacts, public;
\i tests/scripts/contact.sql
\i tests/scripts/borrowing.sql
COMMIT;