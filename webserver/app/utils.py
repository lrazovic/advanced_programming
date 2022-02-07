import os

if "DEV" in os.environ:
    endpoint_fetcher = "http://localhost:5002"
    endpoint_analysis = "http://localhost:5001"
    endpoint_auth = "http://localhost:5003"
    enpdoint_token = "http://localhost"
else:
    endpoint_fetcher = "http://fetcher:5002"
    endpoint_analysis = "http://analysis:5001"
    endpoint_auth = "http://authentication:5003"
    enpdoint_token = "172.17.0.1"

# Webserver definition

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for securing the whole API and managing user authentication",
    },
    {"name": "news_fetcher", "description": "Operations for retrieving RSS news"},
    {
        "name": "ml_processing",
        "description": "Operations for obtaining news textual summary exploiting Natural Language Processing",
    },
    {"name": "dummy", "description": "Just for testing"},
]

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None
