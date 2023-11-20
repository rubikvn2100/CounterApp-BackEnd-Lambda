import json
from session_management import SessionManager


def handle_fetch_counter(event: dict, context) -> dict:
    session_manager = SessionManager(event)

    validation_result = session_manager.validate_session()
    if validation_result["statusCode"] != 200:
        return validation_result

    return session_manager.fetch_counter()
