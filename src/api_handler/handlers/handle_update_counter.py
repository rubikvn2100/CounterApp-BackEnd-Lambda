import json


def handle_update_counter(event: dict, context) -> dict:
    return {"statusCode": 200, "body": json.dumps("Response for POST /api/counter")}
