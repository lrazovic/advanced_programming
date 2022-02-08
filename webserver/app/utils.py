import os

if "DEV" in os.environ:
    endpoint_fetcher = "http://localhost:5002"
    endpoint_analysis = "http://localhost:5001"
    endpoint_auth = "http://localhost:5003"
    enpdoint_token = "http://localhost"
    redirect_uri = "http://localhost:8080/token"
else:
    endpoint_fetcher = "http://fetcher:5002"
    endpoint_analysis = "http://analysis:5001"
    endpoint_auth = "http://authentication:5003"
    enpdoint_token = "172.17.0.1"
    redirect_uri = "http://webserver:3000/token"

redirect_uri = os.environ.get('redirect_uri') or 'http://localhost:8080/token'

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None
