import random

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from hw2.shop_api.db import Cart, CartItem, carts, items


router = APIRouter(prefix="/cart", tags=["cart_api"])


@router.post("/")
async def add_cart():
    cart_id = random.getrandbits(32)
    carts[cart_id] = Cart(id=cart_id)

    return JSONResponse(
        content={"id": cart_id},
        status_code=status.HTTP_201_CREATED,
        headers={"location": f"/cart/{cart_id}"},
    )


@router.get("/{cart_id}")
async def get_cart(cart_id: int):
    if not cart_id in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    return JSONResponse(
        content=carts[cart_id].model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.get("/")
async def get_carts(
    offset: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    min_quantity: float | None = None,
    max_quantity: float | None = None,
):
    if offset < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Offset and limit must be positive",
        )
    for k in (min_price, max_price, min_quantity, max_quantity):
        if k is not None and k < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Price and quantity must be greater than 0",
            )

    carts_list = [carts[k] for k in list(carts.keys())[offset : offset + limit]]
    if min_price is not None:
        carts_list = list(filter(lambda x: x.price >= min_price, carts_list))
    if max_price is not None:
        carts_list = list(filter(lambda x: x.price <= max_price, carts_list))
    if min_quantity is not None:
        carts_list = list(
            filter(
                lambda x: sum(i.quantity for i in x.items) >= min_quantity, carts_list
            )
        )
    if max_quantity is not None:
        carts_list = list(
            filter(
                lambda x: sum(i.quantity for i in x.items) <= max_quantity, carts_list
            )
        )

    return JSONResponse(
        content=[el.model_dump() for el in carts_list],
        status_code=status.HTTP_200_OK,
    )


@router.post("/{cart_id}/add/{item_id}")
async def add_item_to_cart(cart_id: int, item_id: int):
    cart = carts.get(cart_id)
    item = items.get(item_id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if not item or item.deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    cart_item_ids = [x.id for x in carts[cart_id].items]
    if item_id in cart_item_ids:
        for i in carts[cart_id].items:
            if i.id == item_id:
                i.quantity += 1
                break
    else:
        carts[cart_id].items.append(CartItem(id=item.id, name=item.name))

    carts[cart_id].price += item.price

    return JSONResponse(
        content=cart.model_dump(),
        status_code=status.HTTP_200_OK,
    )
