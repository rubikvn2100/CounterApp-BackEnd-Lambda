import json


def handle_create_session(event: dict, context) -> dict:
    return {"statusCode": 200, "body": json.dumps("Response for POST /api/session")}
