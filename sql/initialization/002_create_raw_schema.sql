CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    country TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id INTEGER,
    product_name TEXT,
    category TEXT,
    price NUMERIC(10, 2),
    stock_quantity INTEGER
);

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    status TEXT,
    total_amount NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS raw.order_items (
    order_item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS raw.payments (
    payment_id INTEGER,
    order_id INTEGER,
    payment_date DATE,
    payment_method TEXT,
    amount NUMERIC(12, 2),
    status TEXT
);