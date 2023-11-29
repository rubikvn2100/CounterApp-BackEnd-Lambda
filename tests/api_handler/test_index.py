import json
import os
from unittest.mock import patch
from src.api_handler.index import handle_request


def mock_handler(event, context):
    return {"statusCode": 200, "body": "mock response"}


mock_route_config = {
    "/test_resource": {
        "methods": {
            "TEST": mock_handler,
        }
    }
}


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handle_request():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    context = {}
    expected_response = {"statusCode": 200, "body": "mock response"}

    response = handle_request(event, context)

    assert response == expected_response
