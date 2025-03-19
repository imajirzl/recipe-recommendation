import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

filename = "bbc_recipes_ingredients.txt"
recipes = load_recipes(filename)

user_input = st.text_input("Enter ingredients (comma-separated):", "")

if user_input:
    ingredients = [ingredient.strip() for ingredient in user_input.split(",")]
    
    matching = search_recipes(recipes, ingredients)

    if matching:
        st.subheader("✅ Recipes Found:")
        for recipe in matching:
            st.markdown(f"**[{recipe['title']}]({recipe['link']})**")
            st.write(", ".join(recipe["ingredients"]))  # Show ingredients
            st.write("---")  # Add a separator
    else:
        st.warning("❌ No recipes found with those ingredients.")