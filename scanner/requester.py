import requests
import time
from parser.models import Endpoint


def send_request(endpoint: Endpoint):
    """
    Send HTTP request and capture response metadata.
    """
    start_time = time.time()

    try:
        response = requests.request(
            method=endpoint.method,
            url=endpoint.url,
            headers=endpoint.headers,
            params=endpoint.query_params,
            data=endpoint.body,
            timeout=5
        )

        response_time = time.time() - start_time

        return {
            "status_code": response.status_code,
            "response_time": round(response_time, 3),
            "content_length": len(response.text),
            "text": response.text[:200]  # truncate for readability
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "response_time": None
        }
