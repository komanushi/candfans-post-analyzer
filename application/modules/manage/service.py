import requests


def ping_domain(url: str):
    response = requests.get(url)
    response.raise_for_status()
    print(response.status_code)
