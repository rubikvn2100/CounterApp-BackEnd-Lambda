from decimal import Decimal
from src.api_handler.util.is_valid_timestamp_sequence import is_valid_timestamp_sequence


def test_empty_timestamp_sequence():
    start = Decimal("0")
    end = Decimal("0")
    timestamps = []

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == True


def test_invalid_start():
    start = Decimal("10")
    end = Decimal("0")
    timestamps = [Decimal("0")]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == False


def test_invalid_end():
    start = Decimal("0")
    end = Decimal("0")
    timestamps = [Decimal("10")]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == False


def test_singe_timestamp_sequence_valid_time_frame():
    start = Decimal("0")
    end = Decimal("10")
    timestamps = [Decimal("1")]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == True


def test_unorder_timestamp_sequence():
    start = Decimal("0")
    end = Decimal("10")
    timestamps = [Decimal("2"), Decimal("1"), Decimal("3"), Decimal("4")]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == False


def test_breach_min_duration_threshold():
    start = Decimal("0")
    end = Decimal("10")
    timestamps = [
        Decimal("1"),
        Decimal("1.01"),
        Decimal("1.02"),
        Decimal("2"),
        Decimal("3"),
    ]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == False


def test_valid_long_timestamp_sequence():
    start = Decimal("0")
    end = Decimal("10")
    timestamps = [
        Decimal("1"),
        Decimal("2"),
        Decimal("3"),
    ]

    result = is_valid_timestamp_sequence(start, end, timestamps)

    assert result == True
