import requests
from django.conf import settings

SEARCH_API_KEY = getattr(settings, 'SEARCH_API_KEY', '')
SEARCH_ENGINE_ID = getattr(settings, 'SEARCH_ENGINE_ID', '')

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID
    }
    response = requests.get(url, params=params)
    print(response.json())
    return response.json()
