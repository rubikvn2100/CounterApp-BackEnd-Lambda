import boto3
import json
import os
from .session import Session
from botocore.exceptions import ClientError
from decimal import Decimal


class SessionManager:
    def __init__(self, event: dict):
        dynamodb = boto3.resource("dynamodb")

        self.table_name = os.environ["TABLE_NAME"]
        self.table = dynamodb.Table(self.table_name)

        self.event = event
        self.session = None

    def get_primary_key(self) -> str:
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
