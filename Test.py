import gzip
import base64
import io
import json

def lambda_handler(event, context):
    path = event.get("path", "")

    if "/v1/update_sbom" in path:
        try:
            # Determine if the body is base64 encoded
            is_base64 = event.get("isBase64Encoded", False)

            # Get and decode the request body
            if is_base64:
                compressed_data = base64.b64decode(event["body"])
            else:
                compressed_data = event["body"].encode("utf-8")

            # Decompress gzip data
            buffer = io.BytesIO(compressed_data)
            with gzip.GzipFile(fileobj=buffer, mode="rb") as f:
                decompressed_data = f.read().decode("utf-8")

            # Parse JSON
            sbom_data = json.loads(decompressed_data)

            # Pass to SBOM API logic
            response = sbom_api.update_sbom_for_project(sbom_data)

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response)
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }

    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Not Found"})
    }
