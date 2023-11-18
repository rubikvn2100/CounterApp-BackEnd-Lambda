import time
from decimal import Decimal


def get_current_time() -> Decimal:
    return Decimal(str(time.time()))
