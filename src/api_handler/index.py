route_handlers = {}


def handler(event: dict, context) -> dict:
    http_method = event["httpMethod"]
    resource = event["resource"]

    print(f"Handle {http_method} {resource}")

    handler = route_handlers.get((http_method, resource))

    return handler(event, context)
