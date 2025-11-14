import csv
from datetime import datetime
from pathlib import Path

from sqlmodel import Session

from models import (
    Category,
    Order,
    OrderItem,
    Product,
    User,
    create_db_and_tables,
    engine,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_csv(filename: str) -> list[dict[str, str]]:
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def build_categories(rows: list[dict[str, str]]) -> list[Category]:
    return [Category(id=int(row["id"]), name=row["name"]) for row in rows]


def build_users(rows: list[dict[str, str]]) -> list[User]:
    return [
        User(
            id=int(row["id"]),
            name=row["name"],
            email=row["email"],
            join_date=datetime.fromisoformat(row["join_date"]),
        )
        for row in rows
    ]


def build_products(rows: list[dict[str, str]]) -> list[Product]:
    return [
        Product(
            id=int(row["id"]),
            name=row["name"],
            price=float(row["price"]),
            category_id=int(row["category_id"]),
        )
        for row in rows
    ]


def build_orders(rows: list[dict[str, str]]) -> list[Order]:
    return [
        Order(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            order_date=datetime.fromisoformat(row["order_date"]),
            status=row["status"],
        )
        for row in rows
    ]


def build_order_items(rows: list[dict[str, str]]) -> list[OrderItem]:
    return [
        OrderItem(
            id=int(row["id"]),
            order_id=int(row["order_id"]),
            product_id=int(row["product_id"]),
            quantity=int(row["quantity"]),
        )
        for row in rows
    ]


def ingest():
    create_db_and_tables()

    categories_rows = load_csv("categories.csv")
    users_rows = load_csv("users.csv")
    products_rows = load_csv("products.csv")
    orders_rows = load_csv("orders.csv")
    order_items_rows = load_csv("order_items.csv")

    categories = build_categories(categories_rows)
    users = build_users(users_rows)
    products = build_products(products_rows)
    orders = build_orders(orders_rows)
    order_items = build_order_items(order_items_rows)

    with Session(engine) as session:
        session.add_all(categories)
        session.add_all(users)
        session.add_all(products)
        session.add_all(orders)
        session.add_all(order_items)
        session.commit()

    print(f"Inserted {len(categories)} categories")
    print(f"Inserted {len(users)} users")
    print(f"Inserted {len(products)} products")
    print(f"Inserted {len(orders)} orders")
    print(f"Inserted {len(order_items)} order items")


if __name__ == "__main__":
    ingest()

