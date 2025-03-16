import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase

def get_max_pages(alphabet, base_url):
    page = 1
    while True:
        url = base_url.format(alphabet=alphabet, page=page)
        response = requests.get(url)
        if response.status_code != 200:
            return page - 1 
        page += 1