import math
from urllib.parse import parse_qs

from src.send_response import send_json


def check_int(s):
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


async def factorial(scope, recieve, send):
    query = parse_qs(scope["query_string"])
    n = query.get(b"n")
    if not n or not check_int(n[0].decode()):
        return await send_json(send, 422, {"error": "Unprocessable Entity"})

    if int(n[0].decode()) < 0:
        return await send_json(send, 400, {"error": "Unprocessable Entity"})

    f = math.factorial(int(n[0].decode()))
    return await send_json(send, 200, {"result": f})
    

async def fibonacci(scope, recieve, send):
    def __fibonacci(n):
        if n == 0:
            return 0
        if n in (1, 2):
            return 1
        return __fibonacci(n - 1) + __fibonacci(n - 2)

    path = scope["path"].strip("/").split("/")
    if not check_int(path[1]):
        return await send_json(send, 422, {"error": "Unprocessable Entity"})

    n = int(path[1])
    if n < 0:
        return await send_json(send, 400, {"error": "Unprocessable Entity"})

    f = __fibonacci(n)
    return await send_json(send, 200, {"result": f})


async def mean(scope, recieve, send):
    body = await receive_body(recieve)
    try:
        elem = eval(body)
    except:
        elem = None

    if not type(elem) == list:
        return await send_json(send, 422, {"error": "Unprocessable Entity"})
    if not elem or elem is None:
        return await send_json(send, 400, {"error": "Unprocessable Entity"})
    if not all(type(x) == int or type(x) == float for x in elem):
        return await send_json(send, 422, {"error": "Unprocessable Entity"})

    mean = sum(elem) / len(elem)
    return await send_json(send, 200, {"result": mean})


async def receive_body(receive):
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body
