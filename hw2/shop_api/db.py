from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False


class CartItem(BaseModel):
    id: int
    name: str
    quantity: int = 1


class Cart(BaseModel):
    id: int
    items: list[CartItem] = []
    price: float = 0.0


items: dict[int, Item] = {}
carts: dict[int, Cart] = {}
