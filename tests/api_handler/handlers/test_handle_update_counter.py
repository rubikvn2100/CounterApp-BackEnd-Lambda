import json
from src.api_handler.handlers.handle_update_counter import handle_update_counter
from test_util import create_valid_session_token, set_counter
from util import get_current_time


def test_handle_update_counter_validate_session_failed():
    event = {}
    context = {}

    response = handle_update_counter(event, context)

    assert response["statusCode"] != 200


def test_handle_update_counter_validate_user_activity_failed():
    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}
    context = {}

    response = handle_update_counter(event, context)

    assert response["statusCode"] != 200


def test_handle_update_counter_successful():
    counter = 100
    set_counter(counter)

    token = create_valid_session_token()

    current_time = float(get_current_time())
    timestamps = []

    N = 5
    for i in range(1, N + 1):
        timestamps.append(current_time + 0.15 * i)

    event = {
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps({"timestamps": timestamps}),
    }
    context = {}

    response = handle_update_counter(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response_body["counter"] == counter + N
