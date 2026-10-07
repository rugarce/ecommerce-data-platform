ALTER TABLE raw.customers   ADD COLUMN IF NOT EXISTS _loaded_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE raw.products    ADD COLUMN IF NOT EXISTS _loaded_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE raw.orders      ADD COLUMN IF NOT EXISTS _loaded_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE raw.order_items ADD COLUMN IF NOT EXISTS _loaded_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE raw.payments    ADD COLUMN IF NOT EXISTS _loaded_at TIMESTAMPTZ DEFAULT now();

CREATE TABLE IF NOT EXISTS raw._load_audit (
    audit_id    BIGSERIAL PRIMARY KEY,
    loaded_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    run_id      TEXT,
    table_name  TEXT NOT NULL,
    rows_loaded INTEGER NOT NULL
);