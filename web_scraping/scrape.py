import requests
from bs4 import BeautifulSoup

def extract_links(alphabet, base_url):
    """
    Function to extract all recipe links
    - Input: alphabet (str), base_url (str) = 'https://www.bbc.co.uk/food/recipes/a-z/{alphabet}/{page}#featured-content'
    - Output: list of recipe links
    """
    # initialise empty list
    recipe_links = []
    # define page number, start with 1
    page = 1
    
    while True:
        url = base_url.format(alphabet=alphabet, page=page) # editing base_url according to current alphabet, and current page
        response = requests.get(url)
        
        if response.status_code != 200:
            break # stop if the page does not exist

        html_content = response.content.decode("utf-8", errors="replace")
    
        soup = BeautifulSoup(html_content, "html.parser")

        # extract recipe links
        for div in soup.find_all("div", class_="gel-layout__item"):
            a_tag = div.find("a", class_="promo")
            if a_tag and "href" in a_tag.attrs and "/food/recipes/" in a_tag["href"]:
                link = "https://www.bbc.co.uk" + a_tag["href"]
                recipe_links.append(link) # append extracted link to recipe_links

        # searching if div for pagination exists from soup
        pagination_div = soup.find("div", class_="pagination gel-wrap")
        
        # if no pagination exists, it's a single page result
        if not pagination_div:
            break

        # searching if next button is disabled from pagination_div
        next_button_disabled = pagination_div.find("span", class_="pagination__link pagination__link--disabled gel-pica-bold", string=lambda text: text and "Next" in text)
        
        # if 'next' button is disabled, we're on the last page
        if next_button_disabled:
            break

        page += 1

    # print statement to show how many recipe links are extracted for each alphabet
    print(f"Extracted {len(recipe_links)} links for {alphabet.upper()}")

    return recipe_links

def extract_recipe_details(url):
    """
    Function to extract title and ingredients from individual recipe links
    - Input: url (str) = individual recipe links extracted previously through extract_links()
    - Output: dictionary of recipe details, including title, ingredients, and link
    """
    # initialise empty dictionary
    all_recipes = {}

    response = requests.get(url)

    html_content = response.content.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html_content, "html.parser")
    # extracting title
    title = soup.select_one("h1")

    # if title exists, extract 'text'.
    if title:
        title_text = title.get_text(strip=True)  # Properly extracts and decodes text
    else: # if title does not exist, print the following warning
        print(f"Warning: Title not found for {url}")
        return {}  # return empty dict to skip this entry

    # extract ingredients
    ingredients = {a.get_text(strip=True) for a in soup.select('a[data-testid="ingredient-derived-link"]')}
    
    # if ingredients exist, append to dictionary the following:
    if ingredients:
        all_recipes[title_text] = {
            "ingredients": sorted(ingredients),
            "link": url  
        }
    
    return all_recipes

    

    
