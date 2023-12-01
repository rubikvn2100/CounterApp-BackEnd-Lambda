from .handle_fetch_counter import handle_fetch_counter
from .handle_update_counter import handle_update_counter
from .handle_create_session import handle_create_session

route_config = {
    "/api/session": {
        "methods": {
            "POST": handle_create_session,
        }
    },
    "/api/counter": {
        "methods": {
            "OPTIONS": None,
            "GET": handle_fetch_counter,
            "POST": handle_update_counter,
        },
        "allow_headers": ["Authorization"],
    },
}
