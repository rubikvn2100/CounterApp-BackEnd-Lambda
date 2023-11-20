import boto3
import os


def get_counter() -> int:
    dynamodb = boto3.client("dynamodb")
    get_counter_response = dynamodb.get_item(
        TableName=os.environ["TABLE_NAME"],
        Key={"id": {"S": "counter"}},
    )

    click_count = int(get_counter_response["Item"]["clickCount"]["N"])

    return click_count
