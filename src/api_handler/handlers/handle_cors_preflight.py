import os
from .route_config import route_config
from util import validate_origin


def handle_cors_preflight(event: dict, context) -> dict:
    validation_result = validate_origin(event)
    if validation_result["statusCode"] != 200:
        return validation_result

    origin = validation_result["origin"]

    http_method = event["httpMethod"]
    resource = event["resource"]

    resource = route_config[resource]
    method_names = [method for method in resource["methods"].keys()]
    allow_headers = resource.get("allow_headers", [])

    cors_headers = {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": ", ".join(method_names),
        "Access-Control-Allow-Headers": ", ".join(allow_headers),
        "Access-Control-Max-Age": os.environ["ACCESS_CONTROL_MAX_AGE"],
    }

    return {"statusCode": 200, "headers": cors_headers}
