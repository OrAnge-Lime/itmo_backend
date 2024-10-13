import random
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse


from hw2.shop_api.item_api.contracts import AddItem, AddItemPatch
from hw2.shop_api.db import Item, items


router = APIRouter(prefix="/item", tags=["item_api"])


@router.post("/")
async def add_item(item: AddItem):
    item_id = random.getrandbits(32)
    # TODO
    items[item_id] = Item(id=item_id, name=item.name, price=item.price)

    return JSONResponse(
        content=items[item_id].model_dump(),
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/{item_id}")
async def get_item(item_id: int):
    if not item_id in items or items[item_id].deleted:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse(
        content=items[item_id].model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.get("/")
async def get_items(
    offset: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    show_deleted: bool = False,
):
    if offset < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Offset and limit must be positive",
        )
    if any(k is not None and k < 0 for k in [min_price, max_price]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Price must be non-negative",
        )

    items_list = [items[k] for k in list(items.keys())[offset : offset + limit]]
    if min_price is not None:
        items_list = list(filter(lambda x: x.price >= min_price, items_list))
    if max_price is not None:
        items_list = list(filter(lambda x: x.price <= max_price, items_list))
    if not show_deleted:
        items_list = list(filter(lambda x: not x.deleted, items_list))

    return JSONResponse(
        content=[el.model_dump() for el in items_list],
        status_code=status.HTTP_200_OK,
    )


@router.put("/{item_id}")
async def replace_item(item_id: int, new_item: AddItem):
    if item_id in items:
        new_item = Item(id=item_id, name=new_item.name, price=new_item.price)
        items[item_id] = new_item

        return JSONResponse(
            content=new_item.model_dump(),
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(status_code=404, detail="Item not found")


@router.patch("/{item_id}")
async def change_item(item_id: int, changes: AddItemPatch):
    if item_id in items:
        if items[item_id].deleted:
            return JSONResponse(
                status_code=status.HTTP_304_NOT_MODIFIED, content="Item not found"
            )
        
        new_item = changes.model_dump()
        item = items[item_id].model_dump()

        for k in new_item:
            if new_item[k] is None:
                new_item[k] = item[k]

        new_item = Item(id=item_id, **new_item)
        items[item_id] = new_item

        return JSONResponse(
            content=new_item.model_dump(),
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if item_id in items:
        items[item_id].deleted = True

        return JSONResponse(
            content=items[item_id].model_dump(),
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(status_code=404, detail="Item not found")
