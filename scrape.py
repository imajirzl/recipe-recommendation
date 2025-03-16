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

def extract_links(alphabet, base_url):
    recipe_links = []
    max_pages = get_max_pages(alphabet, base_url)

    for page in range(1, max_pages + 1):
        url = base_url.format(alphabet=alphabet, page=page)
        respose = requests.get(url)

        if response.status_code != 200:
            break # stop if the page does not exist

        soup = BeautifulSoup(response.text, "html.parser")

        # extract recipe links
        for div in soup.find_all("div", class_="gel-layout__item"):
            a_tag = div.find("a", class_="promo")
            if a_tag and "href" in a_tag.attrs:
                link = "https://www.bbc.co.uk" + a_tag["href"]
                recipe_links.append(link)
    
    return recipe_links