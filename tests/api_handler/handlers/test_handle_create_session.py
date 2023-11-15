import json
from src.api_handler.handlers.handle_create_session import handle_create_session


def test_placeholder_create_session():
    event = {}
    context = {}
    expected_response = {
        "statusCode": 200,
        "body": json.dumps("Response for POST /api/session"),
    }

    response = handle_create_session(event, context)

    assert response == expected_response
