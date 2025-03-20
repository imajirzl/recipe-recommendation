# BBC Recipe Scraper & Recipe Recommendation

### Project description
This project scrapes all recipes from https://www.bbc.co.uk/food/recipes, and extracts the ingredients. Then it creates a model that allows the user to input the ingredients they want to use, and returns the links to all recipes that include those ingredients.

### 📦 Dependencies
Make sure you have the following installed before running the app:
```pip install requests beautifulsoup4 streamlit```

### 📁 Repository Structure


### 🚀 How to Run the App
1. Open a terminal in the project folder, where app.py and app_carousel.py is located in.
2. Run one of the following commands:
   For app.py (all results in one page): ```streamlit run app.py```
   For app_carousel.py (one recipe at a time with navigation): ```streamlit run app_carousel.py```
3. Follow the terminal instructions. The app will launch in your browser at:
   ```http://localhost:8501/``` (for app.py)
   ```http://localhost:8502/``` (if running both apps simultaneously).

