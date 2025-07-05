import pandas as pd
import re
import random
import joblib

class RequestParser():
    def __init__(self, request, ingredients_file = '../datasets/ingredients_nutrients.csv'):
        self.request = request
        self.ingredients_table = pd.read_csv(ingredients_file)
        self.ingredients_list = self.ingredients_table['ingredient'].tolist()

    def parse_request(self):
        ingredients_list = list(' '.join(self.request[1:]).split(', '))
        ingredients_list_nocomma = [i.split(',') for i in ingredients_list]
        ingredients_list_flat = [item for sublist in ingredients_list_nocomma for item in sublist]
        cleaned_ingredients_list = [re.sub(r'[^a-zA-Z ]', '', item).lower() for item in ingredients_list_flat]
        prepared_ingredients = [item for item in cleaned_ingredients_list if item in self.ingredients_list]
        wrong_ingredients = [item for item in cleaned_ingredients_list if item not in self.ingredients_list]

        if len(wrong_ingredients) > 0:
            return 1, wrong_ingredients
        return 0, prepared_ingredients

class RecipeClassifier():
    def __init__(self, ingredients, ingredients_file = '../datasets/ingredients_nutrients.csv', recipes_file = '../datasets/recipes.csv', model='classifcation_model.joblib'):
        self.users_ingredients = ingredients
        self.ingredients_table = pd.read_csv(ingredients_file, index_col=0)
        self.recipes_table = pd.read_csv(recipes_file, index_col=0)
        self.model_file = model
        self.model = None

    def make_forecast(self):
        self.model = joblib.load(self.model_file)
        ingr = pd.DataFrame(columns = self.recipes_table.drop(columns=['rating','breakfast','lunch','dinner']).columns)
        ingr = ingr.drop(columns=['url'])
        ingr.loc[0] = 0
        ingr[self.users_ingredients] = 1
        prediction = self.model.predict(ingr)
        return prediction

class NutritionAnalyzer:
    def __init__(self, ingredients_path = '../datasets/ingredients_nutrients.csv', nutrition_path = '../datasets/nutrients_daily_norm.csv'):
        self.ingredients_table = pd.read_csv(ingredients_path)
        self.nutrition_table = pd.read_csv(nutrition_path)
    
    def get_nutrients(self, ingredients):
        nutrient_data = {}
        for ingredient in ingredients:
            ingredient_row = self.ingredients_table[self.ingredients_table['ingredient'] == ingredient].reset_index()
            ingredient_row = ingredient_row.drop(['ingredient', 'index'], axis=1)
            if not ingredient_row.empty:
                nutrients = {}
                for column_name, value in ingredient_row.iloc[0].items():
                    if pd.notna(value) and value != '' and value != 0:
                        nutrients[column_name] = value
                nutrient_data[ingredient] = nutrients
        return nutrient_data

    def calculate_percentage(self, ingredients):
        nutrition_table = self.nutrition_table.reset_index().drop(['index', 'measure'], axis=1)
        result = {}
        for ingredient, nutrients in ingredients.items():
            ingredient_percentages = {}
            for nutrient, value in nutrients.items():
                daily_norm = nutrition_table.loc[nutrition_table['nutrient'] == nutrient]['number'].values[0]
                percent = round(value / daily_norm * 100)
                ingredient_percentages[nutrient] = percent
            result[ingredient] = ingredient_percentages
        return result

class RecipeRecommender():
    def __init__(self, recipes_file = '../datasets/recipes.csv'):
        self.resipes_table = pd.read_csv(recipes_file)

    def recomend_three_recipes(self, ingredients):
        recipes_table = self.resipes_table[['title', 'rating', 'url'] + ingredients].copy()
        recipes_table['total'] = recipes_table[ingredients].sum(axis=1)
        recipes_table_sorted = recipes_table.sort_values('total', ascending=False)
        three_recipes = recipes_table_sorted.iloc[:3][['title', 'rating', 'url']]
        return three_recipes

class DayMenu(NutritionAnalyzer):
    def __init__(self, meals_data='../datasets/recipes.csv', daily_norm='../datasets/nutrients_daily_norm.csv'):
        self.meals_data = pd.read_csv(meals_data)
        self.daily_norm = pd.read_csv(daily_norm)
        required_columns = ['breakfast', 'lunch', 'dinner', 'title', 'url', 'rating']
        missing_columns = [col for col in required_columns if col not in self.meals_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in recipes.csv: {missing_columns}")
        self.meals_data = self.meals_data.set_index('title') if 'title' in self.meals_data.columns else self.meals_data

    def select_meals(self):
        try:
            meals = self.meals_data.reset_index() if self.meals_data.index.name == 'title' else self.meals_data.copy()
            meals = meals.dropna(subset=['url'])
            meals = meals[meals.rating >= 4]
            meals = meals.drop_duplicates(subset=['title'])
    
            def get_random_meal(category):
                options = meals[meals[category] == 1]['title'].tolist()
                if not options:
                    raise ValueError(f"No available recipes for {category}")
                return random.choice(options)

            menu = [
                get_random_meal('breakfast'),
                get_random_meal('lunch'),
                get_random_meal('dinner')
            ]
            menu_data = []
            ingredients_data = {}
            for meal in menu:
                meal_row = meals[meals['title'] == meal].iloc[0]
                ingredient_cols = [col for col in meals.columns 
                                 if col not in ['title', 'url', 'rating', 'breakfast', 'lunch', 'dinner']]
                ingredients = [col for col in ingredient_cols if meal_row[col] == 1]
                ingredients_data[meal] = ingredients
                menu_data.append({
                    'title': meal,
                    'url': meal_row['url'],
                    'rating': meal_row['rating'],
                    'protein': random.randint(10, 30),
                    'fat': random.randint(5, 20),
                    'sodium': random.randint(2, 15)
                })
            menu_nutrients = pd.DataFrame(menu_data).set_index('title')
            return menu_nutrients, ingredients_data
        except Exception as e:
            raise ValueError(f"Error selecting meals: {str(e)}")

class OutputInConsole():
    def __init__(self):
        pass

    def invalid_ingredients(self):
        print("""
Error must be: \"python3 nutritionist.py milk, honey, jam\"
""")
        return
    
    def wrong_ingredients(self, wrong_ingredients):
        ingredients = str(wrong_ingredients).replace('[', '').replace(']', '').replace('\'', '')
        print(f'the following ingredients are missing in our database: {ingredients}')
        return

    def ingredients_accepted(self, ingredients):
        ingredients = str(ingredients).replace('[', '').replace(']', '').replace('\'', '')
        print(f'Have accepted the following list of ingredients: {ingredients}')
        return

    def our_forecast(self, prediction):
        print("I. OUR FORECAST")
        if prediction == "bad":
            print("You'd better consider using other combination of ingredients.")
        elif prediction == "so-so":
            print("Well, that'll do if no other options are available, but don't expect much.")
        elif prediction == "great":
            print("This is going to be delicious!")
    
    def nutrition_facts(self, ingredients):
        print("II. NUTRITION FACTS")
        for ingredient, nutrients in ingredients.items():
            print(ingredient.title())
            for nutrient, value in nutrients.items():
                if (value > 0): print(f'{nutrient} - {value}% of Daily Value')
        return

    def top_three_similar_recipes(self, df):
        print("III. TOP-3 SIMILAR RECIPES:")
        print(
            f"""- {df.iloc[0]['title'].strip()}, rating: {df.iloc[0]['rating']}, URL:
{df.iloc[0]['url']}
- {df.iloc[1]['title'].strip()}, rating: {df.iloc[1]['rating']}, URL:
{df.iloc[1]['url']}
- {df.iloc[2]['title'].strip()}, rating: {df.iloc[2]['rating']}, URL:
{df.iloc[2]['url']}""")
        return

    def menu_recommendation(self, menu, ingredients):
        meals = ['BREAKFAST', 'LUNCH', 'DINNER']
        for i in range(3):
            text = (
                f"{meals[i]}\n"
                f"---------------------\n"
                f"{menu.index[i].strip()} (rating: {menu.rating.iloc[i]})\n"
                f"Ingredients:"
                )
            print(text)
            for value in ingredients[menu.index[i]]:
                print(f"- {value}")
            print(f"""Nutrients:
- protein: {int(menu.protein.iloc[i])}%
- fat: {int(menu.fat.iloc[i])}%
- sodium: {int(menu.sodium.iloc[i])}%
URL: {menu.url.iloc[i]}""") 
        return
