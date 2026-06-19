-- UNSAFE migration — a single destructive change.
--
-- During a rolling deploy the OLD app version is still running while this
-- lands. Each statement below breaks it:
--   * a column rename     -> old code still SELECTs the old name
--   * removing a column   -> old code still references it
--   * a new mandatory col -> fails on existing rows / old INSERTs
--
-- `check_migrations.py` flags every statement below and exits 1. Run:
--   python3 <kit>/tools/check_migrations.py assets/alembic-expand-contract/unsafe.sql

ALTER TABLE users RENAME COLUMN full_name TO display_name;
ALTER TABLE products DROP COLUMN legacy_sku;
ALTER TABLE orders ADD COLUMN status TEXT NOT NULL;
