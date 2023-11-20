import json
import os
import pytest
from src.api_handler.session_management.session_manager import SessionManager
from test_util import (
    create_expired_session_token,
    create_valid_session_token,
    set_counter,
    get_counter,
    get_session,
)
from util import get_current_time


def test_init_session_manager():
    event = {
        "requestContext": {
            "identity": {"sourceIp": "192.168.1.1", "userAgent": "testUserAgent"}
        }
    }

    session_manager = SessionManager(event)

    scan_response = session_manager.table.scan()

    assert session_manager.table_name == "test_database_table"
    assert session_manager.event == event
    assert session_manager.session == None
    assert scan_response["Count"] == 0


def test_get_primary_key():
    event = {
        "requestContext": {
            "identity": {"sourceIp": "192.168.1.1", "userAgent": "testUserAgent"}
        }
    }

    session_manager = SessionManager(event)
    session_manager.create_new_session()

    token = session_manager.session.get_token()
    primary_key = session_manager.get_primary_key()

    assert primary_key == f"TOK#{token}"


def test_get_primary_key_with_token_argument():
    event = {}
    token = "test_token"

    session_manager = SessionManager(event)

    primary_key = session_manager.get_primary_key(token)

    assert primary_key == f"TOK#{token}"


def test_create_new_session():
    event = {
        "requestContext": {
            "identity": {"sourceIp": "192.168.1.1", "userAgent": "testUserAgent"}
        }
    }

    session_manager = SessionManager(event)
    response = session_manager.create_new_session()

    response_body = json.loads(response["body"])
    token = response_body["token"]

    assert response["statusCode"] == 200
    assert len(token) == 32

    scan_response = session_manager.table.scan()
    item = scan_response["Items"][0]

    assert scan_response["Count"] == 1
    assert len(item) == 3
    assert "id" in item
    assert "startTs" in item
    assert "endTs" in item


def test_validate_session_missing_authorization():
    event = {"headers": {}}

    session_manager = SessionManager(event)
    response = session_manager.validate_session()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 401
    assert response_body == "Unauthorized"


def test_validate_session_not_starts_with_bearer():
    event = {"headers": {"Authorization": "test"}}

    session_manager = SessionManager(event)
    response = session_manager.validate_session()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 401
    assert response_body == "Unauthorized"


def test_validate_session_token_not_found():
    event = {"headers": {"Authorization": "Bearer NonExistentToken"}}

    session_manager = SessionManager(event)
    response = session_manager.validate_session()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 404
    assert response_body == "Token not found"


def test_validate_session_token_expired():
    token = create_expired_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}

    session_manager = SessionManager(event)
    response = session_manager.validate_session()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 403
    assert response_body == "Token expired"


def test_validate_session_with_valid_token_and_not_expired():
    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}

    session_manager = SessionManager(event)
    response = session_manager.validate_session()

    assert response["statusCode"] == 200


def test_fetch_counter_bad_request():
    event = {}

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.fetch_counter()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body == "Bad request"


def test_fetch_counter_successful():
    counter = 100
    set_counter(counter)

    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.fetch_counter()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response_body["counter"] == counter


def test_validate_user_activity_no_body():
    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}}

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.validate_user_activity()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body == "Bad request, no body"


def test_validate_user_activity_no_timestamps():
    token = create_valid_session_token()

    event = {"headers": {"Authorization": f"Bearer {token}"}, "body": json.dumps({})}

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.validate_user_activity()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body == "Bad request, no timestamps"


def test_validate_user_activity_unparsable_timestamp():
    token = create_valid_session_token()

    event = {
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps({"timestamps": ["test"]}),
    }

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.validate_user_activity()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body == "Bad request, cannot read timestamps"


def test_validate_user_activity_invalid_timestamps():
    token = create_valid_session_token()

    event = {
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps({"timestamps": ["0", "1"]}),
    }

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.validate_user_activity()

    response_body = json.loads(response["body"])

    assert response["statusCode"] == 422
    assert response_body == "Request cannot be processed"


def test_validate_user_activity_successful():
    token = create_valid_session_token()

    current_time = float(get_current_time())

    event = {
        "headers": {"Authorization": f"Bearer {token}"},
        "body": json.dumps({"timestamps": [current_time + 1, current_time + 2]}),
    }

    session_manager = SessionManager(event)
    session_manager.validate_session()
    response = session_manager.validate_user_activity()

    assert response["statusCode"] == 200


def test_update_counter_successful():
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

    session_manager = SessionManager(event)
    session_manager.validate_session()
    session_manager.validate_user_activity()
    session_manager.update_counter()

    session = get_session(token)
    session_click_count = int(session["clickCount"]["N"])

    assert get_counter() == counter + N
    assert session_click_count == N
