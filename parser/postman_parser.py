import json
from typing import Dict, Any, List
from parser.models import Endpoint
from parser.models import Endpoint, Auth
from urllib.parse import urlparse


class PostmanParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.endpoints: List[Endpoint] = []

    def load_collection(self) -> Dict[str, Any]:
        """
        Load and validate Postman collection JSON file.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Basic validation
            if "item" not in data:
                raise ValueError(
                    "Invalid Postman collection: missing 'item' field")

            return data

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in Postman collection")

    def get_items(self) -> List[Dict[str, Any]]:
        """
        Extract top-level items from the collection.
        """
        data = self.load_collection()
        return data.get("item", [])

    def traverse_items(self, items: List[Dict[str, Any]]):
        """
        Recursively traverse Postman items.
        """
        for item in items:

            # Case 1: Folder (recursive)
            if "item" in item:
                self.traverse_items(item["item"])

            # Case 2: Request
            elif "request" in item:
                endpoint = self._extract_basic_request(item)
                self.endpoints.append(endpoint)

    def _extract_basic_request(self, item: Dict[str, Any]) -> Endpoint:
        request = item.get("request", {})

        name = item.get("name", "Unnamed Request")
        method = request.get("method", "GET")

        url_data = request.get("url", {})
        raw_url = url_data.get("raw", "")
        parsed_url = urlparse(raw_url)

        # Remove query string
        url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        headers = self._parse_headers(request.get("header", []))
        query_params = self._parse_query(url_data.get("query", []))
        body = self._parse_body(request.get("body", {}))
        auth = self._parse_auth(request.get("auth"))

        return Endpoint(
            name=name,
            url=url,
            method=method,
            headers=headers,
            query_params=query_params,
            body=body,
            auth=auth
        )

    def _parse_headers(self, headers_list: List[Dict[str, Any]]) -> Dict[str, str]:
        headers = {}
        for h in headers_list:
            key = h.get("key")
            value = h.get("value")
            if key:
                headers[key] = value
        return headers

    def _parse_query(self, query_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        params = {}
        for q in query_list:
            key = q.get("key")
            value = q.get("value")
            if key:
                params[key] = value
        return params

    def _parse_body(self, body_data: Dict[str, Any]):
        mode = body_data.get("mode")

        if mode == "raw":
            return body_data.get("raw")

        elif mode == "urlencoded":
            return {
                item.get("key"): item.get("value")
                for item in body_data.get("urlencoded", [])
            }

        elif mode == "formdata":
            return {
                item.get("key"): item.get("value")
                for item in body_data.get("formdata", [])
            }

        return None

    def _parse_auth(self, auth_data: Dict[str, Any]) -> Auth:
        if not auth_data:
            return None

        auth_type = auth_data.get("type")

        if auth_type == "bearer":
            token = auth_data.get("bearer", [{}])[0].get("value")
            return Auth(type="bearer", token=token)

        elif auth_type == "apikey":
            key = auth_data.get("apikey", [{}])[0].get("value")
            return Auth(type="apikey", api_key=key)

        return Auth(type=auth_type)
