from parser.postman_parser import PostmanParser


if __name__ == "__main__":
    parser = PostmanParser("collection.json")

    items = parser.get_items()
    parser.traverse_items(items)

    for ep in parser.endpoints:
        print(f"Name: {ep.name}")
        print(f"URL: {ep.url}")
        print(f"Method: {ep.method}")
        print(f"Headers: {ep.headers}")
        print(f"Query Params: {ep.query_params}")
        print(f"Body: {ep.body}")
        print(f"Auth: {ep.auth}")
