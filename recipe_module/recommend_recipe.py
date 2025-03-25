def load_recipes(filename):
    """
    Function to load and parse recipes from the text file 'bbc_recipes_ingredients.txt'
    Input: filename (str) = 'bbc_recipes_ingredients.txt'
    Output: list of dictionaries containing recipe title, link, and set of ingredients
    """
    # initialise empty list
    recipes = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")  # recipes separated by empty lines

    # for each recipe
    for recipe in content:
        lines = recipe.strip().split("\n")
        
        title = lines[0].strip() # first line stores title
        link = lines[1].split("Link: ")[1].strip() # second line stores link to recipe
        ingredients = [line.strip("- ").strip().lower() for line in lines[2:]]  # normalise ingredient format. third and consequent lines stores ingredients

        # append details as a dictionary to recipes
        recipes.append({"title": title, "link": link, "ingredients": set(ingredients)})

    return recipes

def search_recipes(recipes, ingredients):
    """
    Function to finds recipes that contain all the given ingredients
    Input: recipes (list of dictionaries) = extracted from the text file through load_recipes(), ingredients (str) = from user input
    Output: list of recipes that match the input of ingredients from the users
    """
    ingredients = set(ingredient.lower().strip() for ingredient in ingredients)  # normalise input

    matching_recipes = [
        recipe for recipe in recipes if ingredients.issubset(recipe["ingredients"])
    ] # extract recipes where the input ingredients are a subset of the list of ingredients in the recipe

    return matching_recipes
