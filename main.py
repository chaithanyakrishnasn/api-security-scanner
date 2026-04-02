from parser.postman_parser import PostmanParser
from payloads.injector import generate_all_mutations
from scanner.requester import send_request
from analyzer.detector import detect_sqli
from analyzer.detector import detect_xss
from analyzer.detector import detect_status_anomaly, detect_server_error

if __name__ == "__main__":
    parser = PostmanParser("collection.json")

    # Parse collection
    items = parser.get_items()
    parser.traverse_items(items)

    # Process each endpoint
    for ep in parser.endpoints:
        print("\n==============================")
        print(f"Endpoint: {ep.name}")
        print(f"URL: {ep.url}")
        print(f"Method: {ep.method}")

        # Step 1: Baseline request
        print("\n--- BASELINE REQUEST ---")
        baseline_response = send_request(ep)
        print(baseline_response)

        mutations = generate_all_mutations(ep)
        print(f"\nTotal mutations generated: {len(mutations)}")

        # Limit requests for testing
        for i, m in enumerate(mutations[:2], start=1):
            print(f"\n--- Mutation {i} ---")
            print("Query:", m.query_params)
            print("Headers:", m.headers)
            print("Body:", m.body)

            response = send_request(m)

            print("\n--- RESPONSE ---")
            print(response)

            # Detection logic
            vuln_sqli = detect_sqli(response)
            vuln_xss = detect_xss(response)
            vuln_status = detect_status_anomaly(response, baseline_response)
            vuln_error = detect_server_error(response)

            if vuln_status:
                print("\n[!] Status Code Anomaly")
                print(vuln_status)

            if vuln_error:
                print("\n[!] Server Error Detected")
                print(vuln_error)

            if vuln_sqli:
                print("\n[!] SQL Injection Detected")
                print(vuln_sqli)

            if vuln_xss:
                print("\n[!] XSS Detected")
                print(vuln_xss)
