from parser.postman_parser import PostmanParser
from payloads.injector import inject_query_params
from payloads.injector import inject_headers
from payloads.injector import inject_body
from payloads.injector import generate_all_mutations
from scanner.requester import send_request

if __name__ == "__main__":
    parser = PostmanParser("collection.json")

    items = parser.get_items()
    parser.traverse_items(items)

    for ep in parser.endpoints:
        mutations = generate_all_mutations(ep)

        for m in mutations[:2]:  # limit to avoid too many requests
            response = send_request(m)

            print("\n--- RESPONSE ---")
            print(response)
