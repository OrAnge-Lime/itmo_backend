from typing import Any, Awaitable, Callable

from src.router_dict import ROUTER
from src.send_response import send_json


async def application(
    scope: dict[str, Any],
    recieve: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    method = scope["method"]
    path = scope["path"].strip("/").split("/")
    if not path:
        await send_json(send, 404, {'error' : "Not Found"})

    handler = ROUTER.get((path[0], method))
    if not handler:
        await send_json(send, 404, {'error' : "Not Found"})

    await handler(scope, recieve, send)
