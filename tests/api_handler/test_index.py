import json
import os
from unittest.mock import patch
from src.api_handler.index import handler, handle_request, add_cors_headers


def mock_handler(event, context):
    return {"statusCode": 200, "body": "mock response"}


mock_route_config = {
    "/test_resource": {
        "methods": {
            "TEST": mock_handler,
        },
    },
    "/cors_resource": {
        "methods": {
            "OPTIONS": mock_handler,
            "TEST": mock_handler,
        },
        "allow_headers": ["header_1", "header_2"],
    },
}


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handler_validate_origin_failed():
    event = {"headers": {"origin": "https://www.malicious-domain.com"}}
    context = {}

    response = handler(event, context)

    assert response["statusCode"] != 200


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handler_without_origin():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    context = {}
    expected_response = {"statusCode": 200, "body": "mock response"}

    response = handler(event, context)

    assert response == expected_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handler_with_origin():
    allow_origin = "https://www.test-domain.com"
    event = {
        "headers": {"origin": allow_origin},
        "httpMethod": "TEST",
        "resource": "/test_resource",
    }
    context = {}
    expected_response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": allow_origin,
        },
        "body": "mock response",
    }

    response = handler(event, context)

    assert response == expected_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handle_request_options():
    allow_origin = "https://www.test-domain.com"
    event = {
        "headers": {"origin": allow_origin},
        "httpMethod": "OPTIONS",
        "resource": "/api/counter",
    }
    context = {}
    expected_response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Methods": "OPTIONS, GET, POST",
            "Access-Control-Allow-Headers": "Authorization",
            "Access-Control-Max-Age": "3600",
        },
    }

    response = handle_request(event, context)

    print(response)
    print(expected_response)

    assert response == expected_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_handle_request():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    context = {}
    expected_response = {"statusCode": 200, "body": "mock response"}

    response = handle_request(event, context)

    assert response == expected_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_add_cors_headers_with_options():
    event = {"httpMethod": "OPTIONS"}
    input_response = {"statusCode": 200, "body": "Dummy response"}
    origin = "https://www.test-domain.com"

    output_response = add_cors_headers(event, input_response, origin)

    assert output_response == input_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_add_cors_headers_with_headers():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    input_response = {"headers": {"Dummy-Header": "DummyValue"}}
    origin = "https://www.test-domain.com"
    expected_output_response = {
        "headers": {
            "Dummy-Header": "DummyValue",
            "Access-Control-Allow-Origin": origin,
        }
    }

    output_response = add_cors_headers(event, input_response, origin)

    assert output_response == expected_output_response


@patch("src.api_handler.index.route_config", mock_route_config)
def test_add_cors_headers_without_headers():
    event = {"httpMethod": "TEST", "resource": "/test_resource"}
    input_response = {}
    origin = "https://www.test-domain.com"
    expected_output_response = {
        "headers": {
            "Access-Control-Allow-Origin": origin,
        }
    }

    output_response = add_cors_headers(event, input_response, origin)

    assert output_response == expected_output_response
