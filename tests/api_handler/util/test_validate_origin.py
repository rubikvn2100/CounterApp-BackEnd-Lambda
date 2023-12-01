import json
from src.api_handler.util.validate_origin import validate_origin


def test_validate_origin_without_headers():
    event = {}
    expected_response = {"statusCode": 200}

    response = validate_origin(event)

    assert response == expected_response


def test_validate_origin_with_malicious_origin():
    event = {"headers": {"origin": "https://www.malicious-domain.com"}}
    expected_response = {
        "statusCode": 403,
        "body": json.dumps({"message": "Forbidden: Origin not allowed"}),
    }

    response = validate_origin(event)

    assert response == expected_response


def test_validate_origin_with_allow_origin():
    allow_origin = "https://www.test-domain.com"
    event = {"headers": {"origin": allow_origin}}
    expected_response = {"statusCode": 200, "origin": allow_origin}

    response = validate_origin(event)

    assert response == expected_response


def test_validate_origin_without_origin():
    event = {"headers": {}}
    expected_response = {"statusCode": 200}

    response = validate_origin(event)

    assert response == expected_response
