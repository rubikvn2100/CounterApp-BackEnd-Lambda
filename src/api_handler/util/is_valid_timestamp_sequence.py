from decimal import Decimal
from typing import List


def is_valid_timestamp_sequence(
    start: Decimal,
    end: Decimal,
    timestamps: List[Decimal],
    min_duration_threshold: Decimal = Decimal("0.04"),
) -> bool:
    len_timestamps = len(timestamps)

    if len_timestamps == 0:
        return True

    if timestamps[0] < start:
        return False

    if end < timestamps[-1]:
        return False

    if len_timestamps == 1:
        return True

    for i in range(1, len_timestamps):
        if timestamps[i] < timestamps[i - 1]:
            return False

        timestamps_diff = Decimal(timestamps[i] - timestamps[i - 1])
        if timestamps_diff < min_duration_threshold:
            return False

    return True
