import boto3
import json
import os
from .session import Session
from botocore.exceptions import ClientError
from decimal import Decimal
from typing import Optional
from util import get_current_time


class SessionManager:
    def __init__(self, event: dict):
        dynamodb = boto3.resource("dynamodb")

        self.table_name = os.environ["TABLE_NAME"]
        self.table = dynamodb.Table(self.table_name)

        self.event = event
        self.session = None

    def get_primary_key(self, token: Optional[str] = None) -> str:
        if not token:
            token = self.session.get_token()

        return f"TOK#{token}"

    def create_new_session(self) -> dict:
        self.session = Session()
        self.session.create_new_session(self.event)

        try:
            response = self.table.put_item(
                Item={
                    "id": self.get_primary_key(),
                    "startTs": Decimal(str(self.session.get_start_timestamp())),
                    "endTs": Decimal(str(self.session.get_end_timestamp())),
                },
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={
                    "#id": "id",
                },
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                print(f'Error, token "{self.session.get_token()}" already exist')

                return {
                    "statusCode": 409,
                    "body": json.dumps("Request cannot be processed"),
                }
            else:
                raise e

        return {
            "statusCode": 200,
            "body": json.dumps({"token": self.session.get_token()}),
        }

    def validate_session(self) -> dict:
        try:
            token_header = self.event.get("headers", {}).get("Authorization")
            if not token_header or not token_header.startswith("Bearer "):
                raise ValueError("Invalid or missing Authorization header")

            token = token_header.split(" ")[1]
        except Exception as e:
            print(f"Error while extracting token:: {e}")

            return {"statusCode": 401, "body": json.dumps("Unauthorized")}

        response = self.table.get_item(Key={"id": self.get_primary_key(token)})
        item = response.get("Item")

        if not item:
            return {"statusCode": 404, "body": json.dumps("Token not found")}

        if get_current_time() > item["endTs"]:
            return {"statusCode": 403, "body": json.dumps("Token expired")}

        self.session = Session()

        self.session.set_token(token)
        self.session.set_start_timestamp(item["startTs"])
        self.session.set_end_timestamp(item["endTs"])

        return {"statusCode": 200}
