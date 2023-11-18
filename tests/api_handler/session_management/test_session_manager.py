import json
import pytest
from src.api_handler.session_management.session_manager import SessionManager


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
