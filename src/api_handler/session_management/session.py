import hashlib
import os
from decimal import Decimal
from typing import Optional
from util import get_current_time


class Session:
    def __init__(self):
        self.session = {}

        self.session["token"] = None
        self.session["startTs"] = None
        self.session["endTs"] = None
        self.session["clickCount"] = None

    def calculate_end_timestamp(self, current_timestamp: Decimal) -> Decimal:
        return current_timestamp + self.get_session_duration()

    def generate_token(self, event: dict, timestamp: Decimal) -> str:
        identity = event["requestContext"]["identity"]

        source_ip = identity["sourceIp"]
        user_agent = identity["userAgent"]

        join_identity = f"{source_ip}-{user_agent}-{timestamp}"

        hash_identity = hashlib.sha256(join_identity.encode()).hexdigest()
        token = hash_identity[-32:]

        return token

    def create_new_session(self, event: dict) -> None:
        start_timestamp = get_current_time()

        token = self.generate_token(event, start_timestamp)

        end_timestamp = self.calculate_end_timestamp(start_timestamp)

        self.set_token(token)
        self.set_start_timestamp(start_timestamp)
        self.set_end_timestamp(end_timestamp)
        self.set_click_count(0)

    def get_session_duration(self) -> Optional[str]:
        return int(os.environ["SESSION_DURATION"])

    def get_token(self) -> Optional[str]:
        return self.session["token"]

    def get_start_timestamp(self) -> Optional[Decimal]:
        return self.session["startTs"]

    def get_end_timestamp(self) -> Optional[Decimal]:
        return self.session["endTs"]

    def get_click_count(self) -> Optional[int]:
        return self.session["clickCount"]

    def set_token(self, token: str) -> None:
        self.session["token"] = token

    def set_start_timestamp(self, start_timestamp: Decimal) -> None:
        self.session["startTs"] = start_timestamp

    def set_end_timestamp(self, end_timestamp: Decimal) -> None:
        self.session["endTs"] = end_timestamp

    def set_click_count(self, click_count: int) -> None:
        self.session["clickCount"] = click_count
