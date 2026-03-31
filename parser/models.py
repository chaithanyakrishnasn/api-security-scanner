from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class Auth:
    """
    Represents authentication details for an API request.
    """
    type: Optional[str] = None        # e.g., bearer, apikey
    token: Optional[str] = None      # for bearer tokens
    api_key: Optional[str] = None    # for API key auth


@dataclass
class Endpoint:
    """
    Represents a single API endpoint extracted from Postman.
    """
    name: str
    url: str
    method: str

    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, Any] = field(default_factory=dict)
    body: Optional[Any] = None

    auth: Optional[Auth] = None
