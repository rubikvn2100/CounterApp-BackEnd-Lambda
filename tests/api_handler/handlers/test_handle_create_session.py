import boto3
import json
import os
from src.api_handler.handlers.handle_create_session import handle_create_session


def test_handle_create_session_successful():
    event = {
        "requestContext": {
            "identity": {"sourceIp": "192.168.1.1", "userAgent": "testUserAgent"}
        }
    }
    context = {}

    response = handle_create_session(event, context)
    response_body = json.loads(response["body"])
    token = response_body.get("token")

    assert response["statusCode"] == 200
    assert len(token) == 32

    dynamodb = boto3.client("dynamodb")
    get_item_response = dynamodb.get_item(
        TableName=os.environ["TABLE_NAME"], Key={"id": {"S": f"TOK#{token}"}}
    )

    assert "Item" in get_item_response
