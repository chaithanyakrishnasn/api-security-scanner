# API Security Scanner (Postman-Driven Vulnerability Scanner)

A Python-based API security scanner that parses Postman collections, performs automated vulnerability testing (SQLi, XSS, authentication flaws), analyzes API responses, and generates structured security reports.

---

## Features

* **Postman collection parser** for automated API target discovery  
* **Recursive extraction** of nested API requests  
* **Automated payload injection engine** for security testing  
* **SQL Injection (SQLi)** payload fuzzing  
* **Cross-Site Scripting (XSS)** payload testing  
* **Header-based attack simulation** (auth/header manipulation)  
* **Request body fuzzing** for POST/PUT APIs  
* **Baseline response comparison** for anomaly detection  
* **SQL error signature detection**  
* **Reflected XSS detection**  
* **Status code anomaly detection**  
* **Server error exposure detection**  
* **JSON vulnerability report generation**  
* **CLI scan summary reporting**  
* **Modular, production-style Python architecture**  

---

## Current Demo Capabilities

* **Parse Postman collection JSON files**  
* **Extract:**
  * API endpoints
  * HTTP methods
  * Headers
  * Query parameters
  * Request bodies
  * Authentication data
* **Generate payload mutations for:**
  * Query parameters
  * Headers
  * Request body fields
* **Send HTTP requests to API targets**  
* **Capture:**
  * Status codes
  * Response timing
  * Content length
  * Response body snippets
* **Detect:**
  * SQL injection indicators
  * Reflected XSS indicators
  * Status anomalies
  * Server-side error leakage
* **Generate:**
  * JSON vulnerability report
  * Terminal summary report

---

## Project Architecture

```text
api-security-scanner/
│
├── parser/
│   ├── __init__.py
│   ├── models.py              # Endpoint + Auth request models
│   └── postman_parser.py      # Postman collection parser
│
├── payloads/
│   ├── __init__.py
│   ├── payloads.py            # SQLi / XSS payload definitions
│   └── injector.py            # Payload mutation engine
│
├── scanner/
│   ├── __init__.py
│   └── requester.py           # HTTP request execution engine
│
├── analyzer/
│   ├── __init__.py
│   └── detector.py            # Vulnerability detection logic
│
├── reporter/
│   ├── __init__.py
│   ├── models.py              # Vulnerability data model
│   ├── json_reporter.py       # JSON report generator
│   └── cli_reporter.py        # CLI summary report
│
├── config/
│   └── __init__.py
│
├── collection.json            # Input Postman collection
├── main.py                    # Scanner entry point
├── requirements.txt
└── report.json                # Generated report
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/chaithanyakrishnasn/api-security-scanner
cd api-security-scanner
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Add a Postman Collection
Place your exported Postman collection file in the root directory as `collection.json`.

**Export from Postman:**
1. Open your collection
2. Click **Export**
3. Choose **Collection v2.1**
4. Save as `collection.json`

### 4. Run the Scanner
```bash
python main.py
```

---

## Supported Vulnerability Checks

### SQL Injection (SQLi)
**Detects:**
* SQL syntax errors
* MySQL error signatures
* Oracle database errors
* ODBC SQL Server indicators
* Malformed query behavior

**Example payloads:**
* `' OR 1=1 --`
* `' OR '1'='1`
* `'; DROP TABLE users; --`
* `' UNION SELECT NULL, NULL --`

### Cross-Site Scripting (XSS)
**Detects reflected XSS indicators such as:**
* `<script>alert(1)</script>`
* `<img src=x onerror=alert(1)>`

Checks whether malicious payloads are reflected unsanitized in API responses.

### Authentication / Header-Based Testing
**Tests:**
* Authorization header manipulation
* Malformed authentication values
* Header tampering scenarios

**Targets:**
* Broken authentication
* Weak header validation
* Authentication bypass weaknesses

### Input Validation Testing
**Tests malformed input across:**
* Query parameters
* Body fields
* Headers

**Detects:**
* Unexpected server behavior
* Validation failures
* Error leakage

### Status Code Anomaly Detection
Compares baseline responses vs mutated responses.  
**Flags suspicious changes such as:**
* `401` → `200`
* `200` → `500`
* `403` → `200`

**Useful for:**
* Auth bypass detection
* Server instability analysis

### Server Error Exposure
**Detects:**
* Internal server errors
* Stack traces
* Exception leakage
* Traceback disclosures

---

## Scanning Workflow

```text
Postman Collection
        ↓
Collection Parser
        ↓
Endpoint Extraction
        ↓
Payload Mutation Engine
        ↓
HTTP Request Execution
        ↓
Response Analysis
        ↓
Vulnerability Detection
        ↓
JSON + CLI Reporting
```

### Detection Methodology

* **Signature-Based Detection**  
  * *Used for:* SQL Injection  
  * *Detection via:* Database error patterns, known SQL exception signatures  
* **Reflection-Based Detection**  
  * *Used for:* XSS  
  * *Detection via:* Reflected payload inspection  
* **Behavioral Detection**  
  * *Used for:* Status anomalies, unusual response changes  
  * *Detection via:* Baseline comparison  

---

## Example Outputs

### CLI Output
```text
==============================
SCAN SUMMARY
==============================

Total endpoints scanned: 2
Total tests executed: 4
Total vulnerabilities found: 0

Vulnerability Breakdown:
No vulnerabilities detected
```

### JSON Report
```json
[
    {
        "type": "SQL Injection",
        "severity": "High",
        "endpoint": "[https://target-api.com/login](https://target-api.com/login)",
        "method": "POST",
        "payload": "{'username': \"' OR 1=1 --\"}",
        "evidence": "SQL syntax",
        "details": {
            "type": "SQL Injection",
            "severity": "High",
            "pattern": "SQL syntax"
        }
    }
]
```

---

## Core Pipeline

```text
Postman JSON → Endpoint Parsing → Payload Injection
Mutated Requests → HTTP Execution → Response Analysis
Detection Engine → Findings Aggregation → Reporting
```

---

## Technologies Used

* Python
* Requests
* JSON
* Dataclasses
* Regex (`re`)
* `urllib`
* Postman Collection v2.1 format

---

## Security Concepts Demonstrated

This project demonstrates practical API security engineering concepts:
* OWASP API Security fundamentals
* SQL Injection testing
* Reflected XSS detection
* Broken authentication testing
* Input fuzzing
* Response anomaly analysis
* Security reporting
* Modular scanner architecture

---

## Current Limitations

Current implementation limitations:
* Synchronous scanning only
* Limited payload set
* No async concurrency yet
* No OAuth2 authentication support
* No HTML dashboard
* No rate limit detection
* No intelligent payload selection
* No plugin-based vulnerability modules

---

## Future Improvements

Planned enhancements:
* Async scanning with `asyncio` + `httpx`
* Concurrent high-speed scanning
* Rate limit detection
* OAuth2 support
* Bearer token automation
* HTML dashboard reporting
* Streamlit frontend
* Plugin-based vulnerability architecture
* CI/CD pipeline integration
* SARIF export
* SIEM integration
* AI-assisted payload generation
* Smart endpoint classification
* Severity scoring (CVSS-style)
* OWASP API Top 10 mapping
* Authentication bypass heuristics

---

## Best Demo Mode

For best demonstration:
* Use a local intentionally vulnerable API
* Test against sandbox APIs
* Compare clean vs malicious responses
* Inspect generated reports
* Demonstrate detection workflow

**Recommended test environments:**
* OWASP Juice Shop
* DVWA API labs
* Local FastAPI vulnerable demo app

---

## Contributing

Pull requests are welcome. For major changes:
1. Open an issue first
2. Discuss architecture/design changes before implementation

---

> ### Ethical Usage Notice
> This tool is intended for authorized security testing, learning, API hardening, and internal assessment. Do not use against systems you do not own or have explicit permission to test.
```
