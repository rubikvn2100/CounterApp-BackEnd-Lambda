import boto3
import os
from util import get_current_time


def create_valid_session_token() -> str:
    token = "12345678901234567890123456789012"

    current_time = get_current_time()
    session_duration = int(os.environ["SESSION_DURATION"])

    item = {
        "id": {"S": f"TOK#{token}"},
        "startTs": {"N": str(current_time)},
        "endTs": {"N": str(current_time + session_duration)},
    }

    dynamodb = boto3.client("dynamodb")
    dynamodb.put_item(TableName=os.environ["TABLE_NAME"], Item=item)

    return token
