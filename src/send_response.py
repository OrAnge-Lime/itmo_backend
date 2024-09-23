import json


async def send_json(send, status_code, msg):
    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(msg).encode("utf-8"),
        }
    )
