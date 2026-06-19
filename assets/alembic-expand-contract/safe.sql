-- SAFE migration — the EXPAND phase of expand/contract.
--
-- Additive only: both the old and new app versions tolerate this schema, so a
-- rolling deploy is safe. The destructive removals happen later, in a SEPARATE
-- release, after the new code has shipped and any backfill is done.
--
-- `check_migrations.py` exits 0 on this file. Run:
--   python3 <kit>/tools/check_migrations.py assets/alembic-expand-contract/safe.sql

-- Expand: add the new column nullable; the app dual-writes full_name + display_name.
ALTER TABLE users ADD COLUMN display_name TEXT;

-- Expand: NOT NULL is safe ONLY because a DEFAULT covers existing rows + old INSERTs.
ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';

-- Contract (a LATER release, once no running version references the old column,
-- and the backfill is complete). Acknowledged deliberately so the gate allows it:
-- ALTER TABLE products DROP COLUMN legacy_sku;  -- migration-safety: ack legacy_sku unused since v2.0; expand shipped in v1.9
