import csv
import random
from datetime import datetime
from pathlib import Path

from faker import Faker

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def write_csv(file_path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_data() -> None:
    Faker.seed(42)
    random.seed(42)
    fake = Faker()

    fake.unique.clear()
    categories = [
        {"id": idx, "name": fake.unique.word().title()} for idx in range(1, 11)
    ]
    fake.unique.clear()

    users = []
    for idx in range(1, 51):
        join_date = fake.date_time_between(start_date="-3y", end_date="now")
        users.append(
            {
                "id": idx,
                "name": fake.name(),
                "email": fake.unique.email(),
                "join_date": join_date.isoformat(),
            }
        )
    fake.unique.clear()

    products = []
    for idx in range(1, 101):
        products.append(
            {
                "id": idx,
                "name": fake.unique.catch_phrase(),
                "price": f"{random.uniform(5, 500):.2f}",
                "category_id": random.choice(categories)["id"],
            }
        )
    fake.unique.clear()

    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    for idx in range(1, 201):
        user = random.choice(users)
        order_date = fake.date_time_between(
            start_date=datetime.fromisoformat(user["join_date"]),
            end_date="now",
        )
        orders.append(
            {
                "id": idx,
                "user_id": user["id"],
                "order_date": order_date.isoformat(),
                "status": random.choice(statuses),
            }
        )

    order_items = []
    item_id = 1
    product_ids = [product["id"] for product in products]
    for order in orders:
        num_items = random.randint(1, min(5, len(product_ids)))
        for product_id in random.sample(product_ids, k=num_items):
            order_items.append(
                {
                    "id": item_id,
                    "order_id": order["id"],
                    "product_id": product_id,
                    "quantity": random.randint(1, 5),
                }
            )
            item_id += 1

    write_csv(
        DATA_DIR / "categories.csv",
        ["id", "name"],
        categories,
    )
    write_csv(
        DATA_DIR / "users.csv",
        ["id", "name", "email", "join_date"],
        users,
    )
    write_csv(
        DATA_DIR / "products.csv",
        ["id", "name", "price", "category_id"],
        products,
    )
    write_csv(
        DATA_DIR / "orders.csv",
        ["id", "user_id", "order_date", "status"],
        orders,
    )
    write_csv(
        DATA_DIR / "order_items.csv",
        ["id", "order_id", "product_id", "quantity"],
        order_items,
    )


if __name__ == "__main__":
    generate_data()

