def load_recipes(filename):
    """Loads and parses recipes from a text file."""
    recipes = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n\n")  # Recipes separated by empty lines

    for recipe in content:
        lines = recipe.strip().split("\n")
        
        title = lines[0].strip()
        link = lines[1].split("Link: ")[1].strip()
        ingredients = [line.strip("- ").strip().lower() for line in lines[2:]]  # Normalize ingredient format
        
        recipes.append({"title": title, "link": link, "ingredients": set(ingredients)})

    return recipes

def search_recipes(recipes, ingredients):
    """Finds recipes that contain all the given ingredients."""
    ingredients = set(ingredient.lower().strip() for ingredient in ingredients)  # Normalize input

    matching_recipes = [
        recipe for recipe in recipes if ingredients.issubset(recipe["ingredients"])
    ]

    return matching_recipes