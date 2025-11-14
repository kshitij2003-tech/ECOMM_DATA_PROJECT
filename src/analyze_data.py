from collections import defaultdict

from rich.console import Console
from rich.table import Table
from sqlmodel import Session, select

from models import Order, OrderItem, Product, User, engine


def get_top_spenders(limit: int = 10):
    with Session(engine) as session:
        statement = (
            select(
                User.id,
                User.name,
                User.email,
                OrderItem.quantity,
                Product.price,
            )
            .join(Order, Order.user_id == User.id)
            .join(OrderItem, OrderItem.order_id == Order.id)
            .join(Product, Product.id == OrderItem.product_id)
        )
        results = session.exec(statement).all()

    spender_totals: dict[int, dict[str, float | str]] = defaultdict(
        lambda: {"name": "", "email": "", "total": 0.0}
    )
    for user_id, name, email, quantity, price in results:
        spender_totals[user_id]["name"] = name
        spender_totals[user_id]["email"] = email
        spender_totals[user_id]["total"] += quantity * price

    sorted_spenders = sorted(
        spender_totals.items(),
        key=lambda item: item[1]["total"],
        reverse=True,
    )
    return sorted_spenders[:limit]


def display_top_spenders(limit: int = 10) -> None:
    top_spenders = get_top_spenders(limit)

    console = Console()
    table = Table(title="Top Spenders")
    table.add_column("Rank", justify="right", style="cyan", no_wrap=True)
    table.add_column("Customer Name", style="green")
    table.add_column("Email", style="magenta")
    table.add_column("Total Spent ($)", justify="right", style="yellow")

    for idx, (_, info) in enumerate(top_spenders, start=1):
        table.add_row(
            str(idx),
            info["name"],
            info["email"],
            f"{info['total']:.2f}",
        )

    console.print(table)


if __name__ == "__main__":
    display_top_spenders()

