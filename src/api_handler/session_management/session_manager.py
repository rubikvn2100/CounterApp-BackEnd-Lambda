import boto3
import json
import os
from .session import Session
from botocore.exceptions import ClientError
from decimal import Decimal
from typing import Optional
from util import get_current_time, is_valid_timestamp_sequence


class SessionManager:
    def __init__(self, event: dict):
        dynamodb = boto3.resource("dynamodb", region_name=os.environ["AWS_REGION"])

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

    def fetch_counter(self) -> dict:
        if not self.session:
            return {"statusCode": 400, "body": json.dumps("Bad request")}

        get_counter_response = self.table.update_item(
            Key={"id": "counter"},
            UpdateExpression="SET #val = if_not_exists(#val, :default)",
            ExpressionAttributeNames={"#val": "clickCount"},
            ExpressionAttributeValues={":default": 0},
            ReturnValues="ALL_NEW",
        )

        click_count = int(get_counter_response["Attributes"]["clickCount"])

        return {"statusCode": 200, "body": json.dumps({"counter": click_count})}

    def validate_user_activity(self) -> dict:
        try:
            body = json.loads(self.event.get("body", {}))
        except Exception as e:
            print(f"Error extracting timestamps: {e}")

            return {"statusCode": 400, "body": json.dumps("Bad request, no body")}

        try:
            data = body.get("timestamps")
            if not data:
                raise ValueError()
        except Exception as e:
            print(f"Error extracting timestamps: {e}")

            return {
                "statusCode": 400,
                "body": json.dumps("Bad request, no timestamps"),
            }

        try:
            timestamps = [Decimal(str(data_point)) for data_point in data]
        except Exception as e:
            print(f"Error extracting timestamps: {e}")

            return {
                "statusCode": 400,
                "body": json.dumps(f"Bad request, cannot read timestamps"),
            }

        start_timestamp = self.session.get_start_timestamp()
        end_timestamp = self.session.get_end_timestamp()
        if not is_valid_timestamp_sequence(start_timestamp, end_timestamp, timestamps):
            return {
                "statusCode": 422,
                "body": json.dumps("Request cannot be processed"),
            }

        self.session.set_click_count(len(timestamps))

        return {"statusCode": 200}

    def update_counter(self) -> None:
        current_time = get_current_time()

        new_end_timestamp = self.session.calculate_end_timestamp(current_time)
        self.session.set_end_timestamp(new_end_timestamp)

        click_count = self.session.get_click_count()

        transact_items = [
            {
                "Update": {
                    "TableName": self.table_name,
                    "Key": {"id": {"S": "counter"}},
                    "UpdateExpression": "ADD #val :inc",
                    "ExpressionAttributeNames": {"#val": "clickCount"},
                    "ExpressionAttributeValues": {":inc": {"N": str(click_count)}},
                    "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                }
            },
            {
                "Update": {
                    "TableName": self.table_name,
                    "Key": {"id": {"S": self.get_primary_key()}},
                    "UpdateExpression": "SET #endTs = :new_endTs ADD #clickCount :inc",
                    "ExpressionAttributeNames": {
                        "#endTs": "endTs",
                        "#clickCount": "clickCount",
                    },
                    "ExpressionAttributeValues": {
                        ":new_endTs": {"N": str(Decimal(str(new_end_timestamp)))},
                        ":inc": {"N": str(click_count)},
                    },
                    "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                }
            },
        ]

        try:
            dynamodb_client = boto3.client(
                "dynamodb", region_name=os.environ["AWS_REGION"]
            )
            response = dynamodb_client.transact_write_items(
                TransactItems=transact_items
            )
        except Exception as e:
            print(f"Transaction for update counter failed: {e}")
