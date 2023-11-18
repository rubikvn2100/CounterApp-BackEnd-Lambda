import json
from session_management import SessionManager


def handle_create_session(event: dict, context) -> dict:
    session_manager = SessionManager(event)

    return session_manager.create_new_session()
