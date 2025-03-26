import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

# Streamlit app showing recipe recommendations as a carousel: one recipe shown at a time with previous/next buttons

# load recipes from bbc_recipes_ingredients.txt
filename = "bbc_recipes_ingredients.txt"
recipes = load_recipes(filename)

# extract unique ingredients from recipes
all_ingredients = sorted(
    {ingredient for recipe in recipes for ingredient in recipe["ingredients"]}
)

# define user_input field for ingredients. ex input: 'chicken,mozzarella'
user_input = st.multiselect(
    "Select ingredients:", options=all_ingredients, help="Start typing your ingredients"
)

# if there is user input
if user_input:
    # find matching recipes based on input ingredients
    matching = search_recipes(recipes, user_input)

    # if a match exists
    if matching:
        st.subheader(f"✅ {len(matching)} Recipes Found")

        # initialise session state for tracking current recipe index
        if "current_recipe_idx" not in st.session_state:
            st.session_state.current_recipe_idx = 0

        # get current recipe to display
        current_idx = st.session_state.current_recipe_idx
        # Ensure the index is within range
        if matching and 0 <= current_idx < len(matching):
            current_recipe = matching[current_idx]
        else:
            st.warning("No matching recipes found.")
        

        # show current recipe index out of total number of matching recipes
        st.write(f"Recipe {current_idx + 1} of {len(matching)}")

        # define navigation buttons above the recipe box - to avoid users having to scroll down if the ingredient list is long
        col1, col2, col3 = st.columns([1, 2, 1]) # 'size' of each column

        # first column: Previous button
        with col1:
            # if the Previous button is clicked and the current recipe index is larger than 0
            if st.button("⬅ Previous") and st.session_state.current_recipe_idx > 0:
                st.session_state.current_recipe_idx -= 1 # subtract the recipe index by 1, to show previous recipe
        # third column: Next button
        with col3:
            # if the Next button is clicked and the current recipe index is smaller than the last recipe index
            if st.button("Next ➡") and st.session_state.current_recipe_idx < len(matching) - 1:
                st.session_state.current_recipe_idx += 1 # add the recipe index by 1, to show next recipe

        # define recipe box, adding bottom margin of 15 px, style of heading 4 as the recipe title
        st.markdown(
            f"""
            <div style="margin-bottom: 15px;">
                <h4><a href="{current_recipe['link']}" target="_blank">{current_recipe['title']}</a></h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # show ingredients in two columns
        ingredients_list = list(current_recipe["ingredients"])
        col1, col2 = st.columns(2)

        # split the list of ingredients in half. first half in column one and second half in column two
        half = len(ingredients_list) // 2
        with col1:
            for ingredient in ingredients_list[:half]:
                st.write(f"- {ingredient}")

        with col2:
            for ingredient in ingredients_list[half:]:
                st.write(f"- {ingredient}")


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

            # loop through the partial matches and display them in the same carousel format as full matches
            if "current_partial_idx" not in st.session_state:
                st.session_state.current_partial_idx = 0

            # get current partial match to display
            current_partial_idx = st.session_state.current_partial_idx
            current_partial_recipe = partial_matches[current_partial_idx]

            # show current partial match index out of total number of partial matches
            st.write(f"Partial match {current_partial_idx + 1} of {len(partial_matches)}")

            # define navigation buttons for partial matches
            col1, col2, col3 = st.columns([1, 2, 1])  # 'size' of each column

            # first column: Previous button
            with col1:
                if st.button("⬅ Previous") and st.session_state.current_partial_idx > 0:
                    st.session_state.current_partial_idx -= 1  # subtract the partial recipe index by 1, to show previous recipe

            # third column: Next button
            with col3:
                if st.button("Next ➡") and st.session_state.current_partial_idx < len(partial_matches) - 1:
                    st.session_state.current_partial_idx += 1  # add the partial recipe index by 1, to show next recipe

            # display partial recipe details (same as full recipe display)
            st.markdown(
                f"""
                <div style="margin-bottom: 15px;">
                    <h4><a href="{current_partial_recipe['link']}" target="_blank">{current_partial_recipe['title']}</a></h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # show matched ingredients for this partial match
            st.markdown(f"**Matched Ingredients**: {', '.join(current_partial_recipe['matched_ingredients'])}")

            # show ingredients in two columns
            ingredients_list = list(current_partial_recipe["ingredients"])
            col1, col2 = st.columns(2)

            # split the list of ingredients in half. first half in column one and second half in column two
            half = len(ingredients_list) // 2
            with col1:
                for ingredient in ingredients_list[:half]:
                    st.write(f"- {ingredient}")

            with col2:
                for ingredient in ingredients_list[half:]:
                    st.write(f"- {ingredient}")

        else:
            st.warning("❌ No recipes found with those ingredients.")
