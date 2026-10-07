from pathlib import Path
import csv
from datetime import datetime, timedelta
import random


SEED = 42

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "data" / "raw"


def write_csv(filename: str, rows: list[dict], fieldnames: list[str]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with (OUTPUT_DIR / filename).open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers() -> list[dict]:
    customers = []

    first_names = [
        "Ana",
        "Carlos",
        "Laura",
        "Miguel",
        "Sofia",
        "Daniel",
        "Lucia",
        "Pablo",
        "Marta",
        "Javier",
    ]

    last_names = [
        "Garcia",
        "Martin",
        "Lopez",
        "Sanchez",
        "Perez",
        "Gomez",
        "Diaz",
        "Moreno",
        "Navarro",
        "Ruiz",
    ]

    countries = ["Spain", "France", "Portugal", "Italy", "Germany"]

    for customer_id in range(1, 21):
        first_name = first_names[(customer_id - 1) % len(first_names)]
        last_name = last_names[(customer_id - 1) % len(last_names)]

        created_at = datetime(2025, 1, 1) + timedelta(
            days=customer_id * 7
        )

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com",
                "country": countries[(customer_id - 1) % len(countries)],
                "created_at": created_at.isoformat(),
            }
        )

    return customers


def generate_products() -> list[dict]:
    products = [
        {
            "product_id": 1,
            "product_name": "Laptop Pro 14",
            "category": "Electronics",
            "price": "1299.99",
            "stock_quantity": 25,
        },
        {
            "product_id": 2,
            "product_name": "Wireless Mouse",
            "category": "Electronics",
            "price": "29.99",
            "stock_quantity": 150,
        },
        {
            "product_id": 3,
            "product_name": "Mechanical Keyboard",
            "category": "Electronics",
            "price": "89.99",
            "stock_quantity": 80,
        },
        {
            "product_id": 4,
            "product_name": "USB-C Hub",
            "category": "Electronics",
            "price": "49.99",
            "stock_quantity": 120,
        },
        {
            "product_id": 5,
            "product_name": "Monitor 27",
            "category": "Electronics",
            "price": "349.99",
            "stock_quantity": 40,
        },
        {
            "product_id": 6,
            "product_name": "Office Chair",
            "category": "Furniture",
            "price": "249.99",
            "stock_quantity": 35,
        },
        {
            "product_id": 7,
            "product_name": "Standing Desk",
            "category": "Furniture",
            "price": "499.99",
            "stock_quantity": 20,
        },
        {
            "product_id": 8,
            "product_name": "Desk Lamp",
            "category": "Furniture",
            "price": "39.99",
            "stock_quantity": 100,
        },
        {
            "product_id": 9,
            "product_name": "Notebook",
            "category": "Office",
            "price": "8.99",
            "stock_quantity": 300,
        },
        {
            "product_id": 10,
            "product_name": "Backpack",
            "category": "Accessories",
            "price": "59.99",
            "stock_quantity": 75,
        },
    ]

    return products


def generate_orders() -> list[dict]:
    orders = []

    statuses = [
        "completed",
        "completed",
        "completed",
        "pending",
        "cancelled",
    ]

    for order_id in range(1, 31):
        customer_id = ((order_id - 1) % 20) + 1

        order_date = datetime(2025, 2, 1) + timedelta(
            days=order_id
        )

        status = statuses[(order_id - 1) % len(statuses)]

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.date().isoformat(),
                "status": status,
                "total_amount": "0.00",
            }
        )

    return orders


def generate_order_items(products: list[dict]) -> list[dict]:
    items = []

    item_id = 1

    for order_id in range(1, 31):
        product_count = 1 + (order_id % 3)

        selected_products = [
            ((order_id + offset) % len(products)) + 1
            for offset in range(product_count)
        ]

        for product_id in selected_products:
            product = products[product_id - 1]

            quantity = (order_id % 3) + 1

            items.append(
                {
                    "order_item_id": item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": product["price"],
                }
            )

            item_id += 1

    return items


def calculate_order_totals(
    orders: list[dict],
    order_items: list[dict],
) -> None:
    totals = {}

    for item in order_items:
        order_id = item["order_id"]

        amount = (
            float(item["quantity"])
            * float(item["unit_price"])
        )

        totals[order_id] = totals.get(order_id, 0) + amount

    for order in orders:
        order["total_amount"] = f"{totals[order['order_id']]:.2f}"


def generate_payments(orders: list[dict]) -> list[dict]:
    payments = []

    payment_methods = [
        "credit_card",
        "paypal",
        "bank_transfer",
    ]

    for order in orders:
        if order["status"] == "cancelled":
            continue

        payment_status = (
            "completed"
            if order["status"] == "completed"
            else "pending"
        )

        payment_date = datetime.fromisoformat(
            order["order_date"]
        ) + timedelta(days=1)

        payments.append(
            {
                "payment_id": order["order_id"],
                "order_id": order["order_id"],
                "payment_date": payment_date.date().isoformat(),
                "payment_method": payment_methods[
                    (order["order_id"] - 1) % len(payment_methods)
                ],
                "amount": order["total_amount"],
                "status": payment_status,
            }
        )

    return payments


def main() -> None:
    random.seed(SEED)

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders()
    order_items = generate_order_items(products)

    calculate_order_totals(orders, order_items)

    payments = generate_payments(orders)

    write_csv(
        "customers.csv",
        customers,
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "country",
            "created_at",
        ],
    )

    write_csv(
        "products.csv",
        products,
        [
            "product_id",
            "product_name",
            "category",
            "price",
            "stock_quantity",
        ],
    )

    write_csv(
        "orders.csv",
        orders,
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "total_amount",
        ],
    )

    write_csv(
        "order_items.csv",
        order_items,
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
        ],
    )

    write_csv(
        "payments.csv",
        payments,
        [
            "payment_id",
            "order_id",
            "payment_date",
            "payment_method",
            "amount",
            "status",
        ],
    )

    print(f"Raw data generated in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()