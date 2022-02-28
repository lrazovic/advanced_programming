import os

if "DEV" in os.environ:
    endpoint_fetcher = "http://localhost:5002"
    endpoint_newspaper = "http://localhost:5004"
    endpoint_analysis = "http://localhost:5001"
    endpoint_persistence = "http://localhost:5003"
    enpdoint_token = "http://localhost"
    redirect_uri = "http://localhost:8080/token"
else:
    endpoint_fetcher = "http://fetcher:5002"
    endpoint_newspaper = "http://newspaper:5004"
    endpoint_analysis = "http://analysis:5001"
    endpoint_persistence = "http://persistence:5003"
    enpdoint_token = "172.17.0.1"
    redirect_uri = "http://webserver:3000/token"

redirect_uri = os.environ.get("redirect_uri") or "http://localhost:8080/token"

tags_metadata = [
    {"name": "news", "description": "Operations for managing news from RSS feeds"},
    {"name": "users", "description": "Operations for managing users of the system"},
]

# Helper to read numbers using var envs
def cast_to_number(id: str):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None
