from unittest.mock import patch
from src.api_handler.index import handler


def mock_handler(event, context):
    return {"statusCode": 200, "body": "mock response"}


mock_route_handlers = {
    ("TEST", "/test_resource"): mock_handler,
}


@patch("src.api_handler.index.route_handlers", mock_route_handlers)
def test_request():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    context = {}
    expected_response = {"statusCode": 200, "body": "mock response"}

    response = handler(event, context)

    assert response == expected_response
