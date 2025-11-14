from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel, create_engine

DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL, echo=False)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    join_date: datetime = Field(default_factory=datetime.utcnow)

    orders: list["Order"] = Relationship(back_populates="user")


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    products: list["Product"] = Relationship(back_populates="category")


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    category_id: int | None = Field(default=None, foreign_key="category.id")

    category: Category | None = Relationship(back_populates="products")
    order_items: list["OrderItem"] = Relationship(back_populates="product")


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: str

    user: User | None = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="order.id")
    product_id: int | None = Field(default=None, foreign_key="product.id")
    quantity: int

    order: Order | None = Relationship(back_populates="items")
    product: Product | None = Relationship(back_populates="order_items")


def create_db_and_tables(database_url: str | None = None) -> None:
    target_engine = (
        create_engine(database_url, echo=False) if database_url else engine
    )
    SQLModel.metadata.create_all(target_engine)

