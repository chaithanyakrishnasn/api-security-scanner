from copy import deepcopy
from parser.models import Endpoint
from payloads.payloads import SQLI_PAYLOADS


def inject_query_params(endpoint: Endpoint):
    """
    Inject SQLi payloads into query parameters.
    """
    mutated_requests = []

    for param in endpoint.query_params:
        for payload in SQLI_PAYLOADS:
            mutated = deepcopy(endpoint)

            # Inject payload into one parameter at a time
            mutated.query_params[param] = payload

            mutated_requests.append(mutated)

    return mutated_requests


def inject_headers(endpoint: Endpoint):
    """
    Inject SQLi payloads into headers.
    """
    mutated_requests = []

    for header in endpoint.headers:
        for payload in SQLI_PAYLOADS:
            mutated = deepcopy(endpoint)

            # Inject payload into one header at a time
            mutated.headers[header] = payload

            mutated_requests.append(mutated)

    return mutated_requests


def inject_body(endpoint: Endpoint):
    """
    Inject SQLi payloads into JSON body fields.
    """
    mutated_requests = []

    # Only handle dict-like bodies for now
    if not isinstance(endpoint.body, dict):
        return mutated_requests

    for key in endpoint.body:
        for payload in SQLI_PAYLOADS:
            mutated = deepcopy(endpoint)

            # Inject payload into one field at a time
            mutated.body[key] = payload

            mutated_requests.append(mutated)

    return mutated_requests


def generate_all_mutations(endpoint: Endpoint):
    """
    Generate all possible payload mutations for an endpoint.
    """
    all_mutations = []

    # Query params
    all_mutations.extend(inject_query_params(endpoint))

    # Headers
    all_mutations.extend(inject_headers(endpoint))

    # Body
    all_mutations.extend(inject_body(endpoint))

    return all_mutations
