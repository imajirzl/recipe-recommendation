import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

# Streamlit app showing recipe recommendations as one whole page

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
        # if no full matches are found, try partial matches
        partial_matches = []

        for recipe in recipes:
            # find the matched ingredients 
            recipe_ingredients = recipe.get("ingredients", [])
            matched_ingredients = [ingredient for ingredient in user_input if ingredient in recipe_ingredients]

            if matched_ingredients:
                partial_matches.append({
                    'title': recipe['title'],
                    'link': recipe['link'],
                    'matched_ingredients': matched_ingredients,
                    'ingredients': recipe_ingredients,  
                    'matched_count': len(matched_ingredients)  
                })

        if partial_matches:
            # sort partial matches by the number of matched ingredients (descending order)
            partial_matches.sort(key=lambda x: x['matched_count'], reverse=True)

            st.warning("❌ No full matches found, but we found partial matches with the following ingredients:")
            for recipe in partial_matches:
                st.markdown(f"**[{recipe['title']}]({recipe['link']})**")
                st.markdown(f"Matched ingredients: {', '.join(recipe['matched_ingredients'])}")
                st.markdown("\n".join([f"- {ingredient}" for ingredient in recipe['ingredients']]))
                st.write("---")
        
        else:
            st.warning("❌ No recipes found with those ingredients.")
