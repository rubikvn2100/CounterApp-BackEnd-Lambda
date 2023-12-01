import json
import os


def validate_origin(event: dict) -> dict:
    origin = event.get("headers", {}).get("origin", None)

    allow_origins = json.loads(os.environ["ALLOW_ORIGINS"])
    if origin and origin not in allow_origins:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Forbidden: Origin not allowed"}),
        }

    if origin:
        return {"statusCode": 200, "origin": origin}

    return {"statusCode": 200}
