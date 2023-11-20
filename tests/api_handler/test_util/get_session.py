import boto3
import os


def get_session(token: str) -> dict:
    dynamodb = boto3.client("dynamodb")
    get_counter_response = dynamodb.get_item(
        TableName=os.environ["TABLE_NAME"],
        Key={"id": {"S": f"TOK#{token}"}},
    )

    session = get_counter_response["Item"]

    return session
