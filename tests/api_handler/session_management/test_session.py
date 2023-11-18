import os
from decimal import Decimal
from src.api_handler.session_management.session import Session


def test_initialize_session():
    session = Session()

    assert session.get_token() == None
    assert session.get_start_timestamp() == None
    assert session.get_end_timestamp() == None
    assert session.get_click_count() == None


def test_create_new_session():
    event = {
        "requestContext": {
            "identity": {"sourceIp": "192.168.1.1", "userAgent": "testUserAgent"}
        }
    }

    session = Session()

    session.create_new_session(event)

    assert len(session.get_token()) == 32
    assert session.get_click_count() == 0

    start_timestamp = session.get_start_timestamp()
    end_timestamp = session.get_end_timestamp()
    session_duration = int(os.environ["SESSION_DURATION"])

    assert start_timestamp + session_duration == end_timestamp


def test_set_and_get_metho():
    session = Session()

    token = "12345678901234567890123456789012"
    start_timestamp = Decimal("1234567890.123456")
    end_timestamp = Decimal("1234567890.123456")

    session.set_token(token)
    session.set_start_timestamp(start_timestamp)
    session.set_end_timestamp(end_timestamp)
    session.set_click_count(0)

    assert session.get_token() == token
    assert session.get_start_timestamp() == start_timestamp
    assert session.get_end_timestamp() == end_timestamp
    assert session.get_click_count() == 0
