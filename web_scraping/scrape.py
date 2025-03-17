import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase

#def get_max_pages(alphabet, base_url):
#    page = 1
#    while True:
#        url = base_url.format(alphabet=alphabet, page=page)
#        response = requests.get(url)
#        if response.status_code != 200:
#            return min(page - 1, 15) # take only up to 15 pages 
#        page += 1
#    return page

def extract_links(alphabet, base_url, max_pages=15):
    recipe_links = []
    #max_pages = get_max_pages(alphabet, base_url)
    #print(f"{alphabet.upper()}: max pages - {max_pages}")

    for page in range(1, max_pages + 1):
        url = base_url.format(alphabet=alphabet, page=page)
        response = requests.get(url)

        if response.status_code != 200:
            break # stop if the page does not exist

        soup = BeautifulSoup(response.text, "html.parser")

        # extract recipe links
        for div in soup.find_all("div", class_="gel-layout__item"):
            a_tag = div.find("a", class_="promo")
            if a_tag and "href" in a_tag.attrs:
                link = "https://www.bbc.co.uk" + a_tag["href"]
                recipe_links.append(link)
                
    print(f"Extracted {len(recipe_links)} links for {alphabet.upper()}")
    
    return recipe_links

def extract_recipe_details(url):
    all_recipes = {}

    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    title = soup.select_one("h1")
    ingredients = {a.text.strip() for a in soup.select('a[data_testid="ingredient-derived-link"]')}

    if ingredients:
        return title.text.strip(), sorted(ingredients)
    return None, None

    