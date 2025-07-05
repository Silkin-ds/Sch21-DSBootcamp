import sys
from recipes import RequestParser, RecipeClassifier, NutritionAnalyzer, RecipeRecommender, OutputInConsole, DayMenu

def main():
    output = OutputInConsole()
    if len(sys.argv) == 2 and sys.argv[1] == 'menu':        
        rec_menu, ingredients_for_rec_menu = DayMenu().select_meals()
        output.menu_recommendation(rec_menu, ingredients_for_rec_menu)
        return

    if len(sys.argv) > 1:
        rp = RequestParser(sys.argv)
        status, ingredients = rp.parse_request()
        if status == 1:
            output.wrong_ingredients(ingredients)
            return

    if (len(sys.argv) == 1 or len(ingredients) < 1):
        output.invalid_ingredients()
        return

    rc = RecipeClassifier(ingredients)
    prediction = rc.make_forecast()
    output.our_forecast(prediction)
    na = NutritionAnalyzer()
    nutrients = na.get_nutrients(ingredients)
    output.nutrition_facts(nutrients)
    rr = RecipeRecommender()
    three_recipes = rr.recomend_three_recipes(ingredients)
    output.top_three_similar_recipes(three_recipes)
    return

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
