import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from hw2.shop_api.item_api.item_router import router as irouter
from hw2.shop_api.cart_api.cart_router import router as crouter


app = FastAPI(
    title="HW_2_Backend",
    description="Homework 2",
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
)

app.state.Logger = logging.getLogger(name="hw2")
app.state.Logger.setLevel("DEBUG")

app.include_router(irouter)
app.include_router(crouter)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Middleware function that manages the database
    session for each incoming request and closes
    the session after the response is sent.

    Args:
        request (Request): The incoming request object.

        call_next (function): The function to call
        the next middleware or the main application handler.

    Returns:
        Response: The response object returned by the
        next middleware or the main application handler.
    """
    try:
        response = await call_next(request)
    except Exception as exc:
        detail = getattr(exc, "detail", None)
        unexpected_error = not detail
        if unexpected_error:
            args = getattr(exc, "args", None)
            detail = args[0] if args else str(exc)
        app.state.Logger.error(detail, exc_info=unexpected_error)
        status_code = getattr(exc, "status_code", 500)
        response = JSONResponse(
            content={"detail": str(detail), "success": False}, status_code=status_code
        )

    return response


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8020,
    )
