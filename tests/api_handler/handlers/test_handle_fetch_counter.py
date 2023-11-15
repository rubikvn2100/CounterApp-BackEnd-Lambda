import json
from src.api_handler.handlers.handle_fetch_counter import handle_fetch_counter


def test_placeholder_fetch_counter():
    event = {}
    context = {}
    expected_response = {
        "statusCode": 200,
        "body": json.dumps("Response for GET /api/counter"),
    }

    response = handle_fetch_counter(event, context)

    assert response == expected_response
