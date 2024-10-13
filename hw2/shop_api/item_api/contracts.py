from pydantic import BaseModel


class AddItem(BaseModel):
    name: str
    price: float


class AddItemPatch(BaseModel):
    name: str = None
    price: float = None

    class Config:
        extra = "forbid"
