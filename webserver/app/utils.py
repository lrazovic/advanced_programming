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
