import re


SQL_ERROR_PATTERNS = [
    r"SQL syntax",
    r"mysql_fetch",
    r"ORA-",
    r"syntax error",
    r"unclosed quotation mark",
    r"ODBC SQL Server",
]


def detect_sqli(response: dict):
    """
    Detect possible SQL injection from response.
    """
    if "text" not in response:
        return None

    text = response["text"]

    for pattern in SQL_ERROR_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "type": "SQL Injection",
                "severity": "High",
                "pattern": pattern
            }

    return None


XSS_PAYLOAD_MARKERS = [
    "<script>alert(1)</script>",
    "onerror=alert(1)",
    "<img src=x"
]


def detect_xss(response: dict):
    """
    Detect possible reflected XSS in response.
    """
    if "text" not in response:
        return None

    text = response["text"]

    for marker in XSS_PAYLOAD_MARKERS:
        if marker.lower() in text.lower():
            return {
                "type": "XSS",
                "severity": "High",
                "evidence": marker
            }

    return None


def detect_status_anomaly(response: dict, baseline: dict):
    """
    Detect abnormal status code changes compared to baseline.
    """
    if "status_code" not in response or "status_code" not in baseline:
        return None

    if response["status_code"] != baseline["status_code"]:
        return {
            "type": "Status Code Anomaly",
            "severity": "Medium",
            "baseline": baseline["status_code"],
            "current": response["status_code"]
        }

    return None


ERROR_PATTERNS = [
    "internal server error",
    "exception",
    "stack trace",
    "traceback",
    "unexpected error"
]


def detect_server_error(response: dict):
    """
    Detect generic server-side errors.
    """
    if "text" not in response:
        return None

    text = response["text"].lower()

    for pattern in ERROR_PATTERNS:
        if pattern in text:
            return {
                "type": "Server Error Exposure",
                "severity": "Medium",
                "pattern": pattern
            }

    return None
