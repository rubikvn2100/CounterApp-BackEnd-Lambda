import boto3
import os


def set_counter(counter: int) -> None:
    item = {"id": {"S": "counter"}, "clickCount": {"N": str(counter)}}

    dynamodb = boto3.client("dynamodb", region_name=os.environ["AWS_REGION"])
    dynamodb.put_item(TableName=os.environ["TABLE_NAME"], Item=item)
