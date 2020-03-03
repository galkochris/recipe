from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json
import time
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()


apikey = os.getenv("API_KEY")


app = Flask(__name__)

@app.route('/')
def index():
#     url = "https://api.spoonacular.com/recipes/random"

#     params = {
#         'number': 3,
#         'apiKey': apikey
#     }

#     r = requests.get(url, params=params)
#     json_recipes = json.loads(r.content)
#     recipes = json_recipes['recipes']

#     return render_template('index.html', recipes=recipes)
    return render_template('test.html')




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

    instructions_params = {
        'apiKey': apikey
    }
    instructions_url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"

    req = requests.get(instructions_url, params=instructions_params)
    if req.status_code == 200:
        json_instructions = json.loads(req.content)
        steps = json_instructions[0]["steps"]
    else:
        return "error"
    return render_template('single_recipe.html', ingredients=ingredients, steps=steps, recipe_id=id)

    
    