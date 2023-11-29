import json
import os
from handlers import route_config


def handler(event: dict, context) -> dict:
    response = handle_request(event, context)

    return response


def handle_request(event: dict, context) -> dict:
    http_method = event["httpMethod"]
    resource = event["resource"]

    print(f"Handle {http_method} {resource}")

    handler = route_config[resource]["methods"][http_method]

    return handler(event, context)
