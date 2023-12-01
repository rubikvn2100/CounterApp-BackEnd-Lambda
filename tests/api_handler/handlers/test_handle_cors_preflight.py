import os
from src.api_handler.handlers.handle_cors_preflight import handle_cors_preflight


def test_handle_cors_preflight_validate_origin_failed():
    event = {"headers": {"origin": "https://www.malicious-domain.com"}}
    context = {}

    response = handle_cors_preflight(event, context)

    assert response["statusCode"] != 200


def test_handle_cors_preflight_validate_origin_successful():
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

    response = handle_cors_preflight(event, context)

    assert response == expected_response
