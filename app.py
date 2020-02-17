from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


apikey = os.getenv("API_KEY")


app = Flask(__name__)

@app.route('/')
def index():
    url = "https://api.spoonacular.com/recipes/random"

    params = {
        'number': 4,
        'apiKey': apikey
    }

    r = requests.get(url, params=params)
    json_recipes = json.loads(r.content)
    recipes = json_recipes['recipes']

    return render_template('index.html', recipes=recipes)

@app.route('/recipe')
def recipe():


    search_term = request.args.get('user_input')


    params = {
        'query': search_term,
        'apiKey': apikey,
        'number': 6
    }

    url = "https://api.spoonacular.com/recipes/search"


    r = requests.get(url, params=params)
    if r.status_code == 200:
        json_recipes = json.loads(r.content)
        recipes = json_recipes['results']
        return render_template('recipe.html', recipes=recipes)



@app.route('/recipe/<id>')
def display_single_recipe(id):
    params = {
        'id': id,
        "apiKey": apikey
    }
    url = f"https://api.spoonacular.com/recipes/{id}/information"
    r = requests.get(url, params=params)
    if r.status_code == 200:
        json_recipe = json.loads(r.content)
        ingredients = json_recipe['extendedIngredients']
    else:
        return "error"
    return render_template('single_recipe.html', ingredients=ingredients)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    
    