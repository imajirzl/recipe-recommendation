import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

"""Streamlit app showing recipe recommendations as one whole page"""

# load recipes from bbc_recipes_ingredients.txt
filename = "bbc_recipes_ingredients.txt"
recipes = load_recipes(filename)

# extract unique ingredients from recipes
all_ingredients = sorted(
    {ingredient for recipe in recipes for ingredient in recipe["ingredients"]}
)

# user_input field for ingredients, creating a searchable dropdown for ingredients
user_input = st.multiselect(
    "Select ingredients:", options=all_ingredients, help="Start typing your ingredients"
)

# if there is user input
if user_input:
    # find matching recipes based on input ingredient
    matching = search_recipes(recipes, user_input)

    # if a match exists
    if matching:
        st.subheader("✅ Recipes Found:")
        for recipe in matching:
            st.markdown(f"**[{recipe['title']}]({recipe['link']})**")  # show title with hyperlink
            st.markdown("\n".join([f"- {ingredient}" for ingredient in recipe["ingredients"]]))  # show ingredients as bullets
            st.write("---")  # Separator
    else:
        st.warning("❌ No recipes found with those ingredients.")
