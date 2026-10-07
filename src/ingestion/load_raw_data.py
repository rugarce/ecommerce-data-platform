import csv
import logging
import os
import sys
from pathlib import Path

import psycopg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("load_raw_data")


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

RUN_ID = os.getenv("AIRFLOW_CTX_DAG_RUN_ID", "manual")
DB_CONFIG = {
    "host": "postgres",
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "ecommerce"),
    "user": os.getenv("POSTGRES_USER", "ecommerce_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "ecommerce_password"),
}


TABLES = {
    "customers.csv": {
        "table": "raw.customers",
        "columns": [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "country",
            "created_at",
        ],
    },
    "products.csv": {
        "table": "raw.products",
        "columns": [
            "product_id",
            "product_name",
            "category",
            "price",
            "stock_quantity",
        ],
    },
    "orders.csv": {
        "table": "raw.orders",
        "columns": [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "total_amount",
        ],
    },
    "order_items.csv": {
        "table": "raw.order_items",
        "columns": [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
        ],
    },
    "payments.csv": {
        "table": "raw.payments",
        "columns": [
            "payment_id",
            "order_id",
            "payment_date",
            "payment_method",
            "amount",
            "status",
        ],
    },
}

class ValidationError(Exception):
    pass

def read_csv(filename: str, columns: list[str]) -> list[tuple]:
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise ValidationError(f"{filename}: no existe {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        missing = [c for c in columns if c not in (reader.fieldnames or [])]
        if missing:
            raise ValidationError(f"{filename}: faltan columnas {missing}")

        rows = []
        for line_number, row in enumerate(reader, start=2):
            values = tuple(row[c] for c in columns)
            if any(v is None for v in values):
                raise ValidationError(
                    f"{filename}: línea {line_number} con menos campos de los esperados"
                )
            rows.append(values)

    if not rows:
        raise ValidationError(f"{filename}: no contiene filas de datos")

    return rows


def load_table(cursor, table: str, columns: list[str], rows: list[tuple]) -> None:
    cursor.execute(f"TRUNCATE TABLE {table}")

    placeholders = ", ".join(["%s"] * len(columns))
    column_list = ", ".join(columns)
    cursor.executemany(
        f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})",
        rows,
    )


def main() -> int:
    # Fase 1: validar todo antes de tocar la base de datos
    data = {}
    try:
        for filename, config in TABLES.items():
            data[filename] = read_csv(filename, config["columns"])
    except ValidationError as exc:
        log.error("Validación fallida, la base de datos no se ha modificado: %s", exc)
        return 1

    # Fase 2: una única transacción para las cinco tablas
    try:
        with psycopg.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                for filename, config in TABLES.items():
                    rows = data[filename]
                    load_table(cursor, config["table"], config["columns"], rows)
                    cursor.execute("INSERT INTO raw._load_audit (run_id, table_name, rows_loaded) VALUES (%s, %s, %s)",
                                   (RUN_ID, config["table"], len(rows)),)
                    log.info("Loaded %s rows into %s", len(rows), config["table"])
    except psycopg.Error as exc:
        log.error("Carga fallida, se ha hecho rollback de todas las tablas: %s", exc)
        return 1

    log.info("Carga completada")
    return 0


if __name__ == "__main__":
    sys.exit(main())