from parser.postman_parser import PostmanParser
from payloads.injector import inject_query_params
from payloads.injector import inject_headers
from payloads.injector import inject_body
from payloads.injector import generate_all_mutations

if __name__ == "__main__":
    parser = PostmanParser("collection.json")

    items = parser.get_items()
    parser.traverse_items(items)

    for ep in parser.endpoints:
        print("\n==============================")
        print(f"Endpoint: {ep.name}")

        mutations = generate_all_mutations(ep)

        print(f"Total mutations generated: {len(mutations)}")

        for m in mutations:
            print("----")
            print("Query:", m.query_params)
            print("Headers:", m.headers)
            print("Body:", m.body)
