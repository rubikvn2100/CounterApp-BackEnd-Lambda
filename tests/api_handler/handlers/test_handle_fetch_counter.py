import json
import os
from src.api_handler.handlers.handle_fetch_counter import handle_fetch_counter
from test_util import create_valid_session_token, set_counter


def test_handle_fetch_counter_validate_session_failed():
    event = {}
    context = {}

    response = handle_fetch_counter(event, context)

    assert response["statusCode"] != 200


def test_handle_fetch_counter_successful():
    counter = 100
    set_counter(counter)

    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}
    context = {}

    response = handle_fetch_counter(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response_body["counter"] == counter
