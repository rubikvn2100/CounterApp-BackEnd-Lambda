from handlers import *

route_handlers = {
    ("GET", "/api/counter"): handle_fetch_counter,
    ("POST", "/api/counter"): handle_update_counter,
    ("POST", "/api/session"): handle_create_session,
}


def handler(event: dict, context) -> dict:
    http_method = event["httpMethod"]
    resource = event["resource"]

    print(f"Handle {http_method} {resource}")

    handler = route_handlers.get((http_method, resource))

    return handler(event, context)
