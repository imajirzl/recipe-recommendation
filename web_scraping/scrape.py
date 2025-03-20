import requests
from bs4 import BeautifulSoup

def extract_links(alphabet, base_url):
    recipe_links = []
    page = 1
    
    while True:
        url = base_url.format(alphabet=alphabet, page=page)
        response = requests.get(url)

        if response.status_code != 200:
            break # stop if the page does not exist

        soup = BeautifulSoup(response.text, "html.parser")

        # extract recipe links
        for div in soup.find_all("div", class_="gel-layout__item"):
            a_tag = div.find("a", class_="promo")
            if a_tag and "href" in a_tag.attrs and "/food/recipes/" in a_tag["href"]:
                link = "https://www.bbc.co.uk" + a_tag["href"]
                recipe_links.append(link)
        
        pagination_div = soup.find("div", class_="pagination gel-wrap")
        
        # if no pagination exists, it's a single page result
        if not pagination_div:
            break

        next_button_disabled = pagination_div.find("span", class_="pagination__link pagination__link--disabled gel-pica-bold", string=lambda text: text and "Next" in text)
        
        # if 'next' button is disabled, we're on the last page
        if next_button_disabled:
            break

        page += 1
        first_page = False # after first page, no longer skip the check
                
    print(f"Extracted {len(recipe_links)} links for {alphabet.upper()}")

    return recipe_links

def extract_recipe_details(url):
    all_recipes = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("h1")

    if title:
        title_text = title.text.strip()
    else: 
        print(f"Warning: Title not found for {url}")
        return {}  # Return empty dict to skip this entry

    ingredients = {a.text.strip() for a in soup.select('a[data-testid="ingredient-derived-link"]')}

    if ingredients:
        all_recipes[title_text] = {
            "ingredients": sorted(ingredients),
            "link": url  
        }
    
    return all_recipes

    
