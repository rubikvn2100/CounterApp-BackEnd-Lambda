import json
import os
from handlers import route_config, handle_cors_preflight
from util import validate_origin


def handler(event: dict, context) -> dict:
    validation_result = validate_origin(event)
    if validation_result["statusCode"] != 200:
        return validation_result

    response = handle_request(event, context)

    origin = validation_result.get("origin", None)
    if origin:
        response = add_cors_headers(event, response, origin)

    return response


def handle_request(event: dict, context) -> dict:
    http_method = event["httpMethod"]
    resource = event["resource"]

    print(f"Handle {http_method} {resource}")

    if http_method == "OPTIONS":
        handler = handle_cors_preflight
    else:
        handler = route_config[resource]["methods"][http_method]

    return handler(event, context)


def add_cors_headers(event: dict, response: dict, origin: str) -> dict:
    if event["httpMethod"] == "OPTIONS":
        return response

    cors_headers = {"Access-Control-Allow-Origin": origin}

    response["headers"] = {**response.get("headers", {}), **cors_headers}

    return response
