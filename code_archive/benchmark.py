# Connection to external data sources (e.g., APIs)
import requests

def fetch_benchmark_indices(api_url):
    response = requests.get(api_url)
    benchmark_indices = response.json()
    return benchmark_indices
