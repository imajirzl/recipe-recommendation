import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

"""Streamlit app showing recipe recommendations as one whole page"""
# ADD definition
# load recipes from bbc_recipes_ingredients.txt
filename = "bbc_recipes_ingredients.txt"
recipes = load_recipes(filename)

# define user_input field for ingredients. ex input: 'chicken,mozzarella'
user_input = st.text_input("Enter ingredients (comma-separated):", "")

# if there is user input
if user_input:
    # turn input of ingredients into list: split by commas and remove extra spaces
    ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

    # find matching recipes based on input ingredients
    matching = search_recipes(recipes, ingredients)

    # if a match exists
    if matching:
        st.subheader("✅ Recipes Found:")
        for recipe in matching: # for each recipe in found matching recipes
            st.markdown(f"**[{recipe['title']}]({recipe['link']})**") # show title hyperlinked to the corresponding recipe link
            st.markdown("\n".join([f"- {ingredient}" for ingredient in recipe["ingredients"]])) # show ingredients as bullet points
            st.write("---")  # add a separator after each recipe
    else:
        st.warning("❌ No recipes found with those ingredients.")
