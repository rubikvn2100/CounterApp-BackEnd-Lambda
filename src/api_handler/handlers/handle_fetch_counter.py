import json


def handle_fetch_counter(event: dict, context) -> dict:
    return {"statusCode": 200, "body": json.dumps("Response for GET /api/counter")}
