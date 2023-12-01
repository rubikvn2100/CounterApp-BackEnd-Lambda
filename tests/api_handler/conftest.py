import boto3
import pytest
import os
from moto import mock_dynamodb

TABLE_NAME = "test_database_table"
AWS_REGION = "us-west-1"
SESSION_DURATION = "10"


@pytest.fixture(autouse=True)
def set_aws_env():
    os.environ["AWS_REGION"] = AWS_REGION

    yield

    del os.environ["AWS_REGION"]


@pytest.fixture(autouse=True)
def set_mock_aws_lambda_env():
    os.environ["TABLE_NAME"] = TABLE_NAME
    os.environ["SESSION_DURATION"] = SESSION_DURATION

    yield

    del os.environ["TABLE_NAME"]
    del os.environ["SESSION_DURATION"]


@pytest.fixture(autouse=True)
def create_mock_database_table():
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

        yield
