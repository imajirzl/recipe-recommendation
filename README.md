# BBC Recipe Scraper & Recipe Recommendation

## Project description
This project scrapes all recipes from https://www.bbc.co.uk/food/recipes, and extracts the ingredients. Then it creates a model that allows the user to input the ingredients they want to use, and returns the links to all recipes that include those ingredients.

## 📦 Dependencies
Make sure you have the following installed before running the app:
```pip install requests beautifulsoup4 streamlit```

## 📁 Repository Structure
### Modules
#### Web Scraping
**Purpose**: Scrapes recipes from the BBC Food website.
**Functions**:
  1. ```extract_links()```: Extracts recipe links for all alphabets (A-Z) and all pages per alphabet.
  - Input: alphabet, base_url
  - ```base_url = "https://www.bbc.co.uk/food/recipes/a-z/{alphabet}/{page}#featured-content"```
  - Output: List of recipe links
  
  2. ```extract_recipe_details()```: Extracts the title and ingredients from each recipe link.
  - Input: Recipe URL.
  - Output: Dictionary with:
      - title: Recipe name.
      - link: URL of the recipe.
      - ingredients: List of ingredients.
 
#### Recipe Matching
**Purpose**: Matches user-inputted ingredients with saved recipes.
**Functions**:
   1. ```load_recipes()```: Loads and parses recipes from the saved text file of the recipe links.
   - Input: Filepath.
   - Output: List of dictionaries containing:
       - title: Recipe name.
       - link: URL of the recipe.
       - ingredients: Set of ingredients.
   2. ```search_recipes()```: Finds recipes that contain all of the given ingredients.
   - Input: recipes (from load_recipes), ingredients (from user input).
   - Output: List of matching recipes.

### Notebooks
1. ```notebook_iterations/``` → Initial runs for web scraping & matching (moved to modules).
2. ```run_scraping.ipynb``` → Notebook to test web scraping modules.

### Text Files
1. ```recipe_links.txt``` → Output from ```extract_links()``` (list of recipe links), run through ```run_scraping.ipynb```.
2. ```bbc_recipes_ingredients.txt``` → Output from ```extract_recipe_details()``` (parsed recipes with ingredients), run through ```run_scraping.ipynb```.

### Streamlit Apps
There are two different versions of the developed interface:
1. ```app.py``` → Displays all matching recipes on a single page.
2. ```app_carousel.py``` → Displays recipes one by one, with next/previous buttons. Also shows the total number of matching recipes


## 🚀 How to Run the App
1. Open a terminal in the project folder, where ```app.py``` and ```app_carousel.py``` is located in.
2. Run one of the following commands:

   For app.py (all results in one page): ```streamlit run app.py```

   For app_carousel.py (one recipe at a time with navigation): ```streamlit run app_carousel.py```
4. Follow the terminal instructions. The app will launch in your browser at:

   ```http://localhost:8501/``` (for app.py)

   ```http://localhost:8502/``` (if running both apps simultaneously).

