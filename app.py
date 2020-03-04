from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json
import time
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()


apikey = os.getenv("API_KEY")


app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    url = "https://api.spoonacular.com/recipes/random"

    params = {
        'number': 3,
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
        'number': 1
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
        image = json_recipe['image']
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
    return render_template('single_recipe.html', ingredients=ingredients, steps=steps, recipe_id=id, image=image)

@app.route('/<id>/text', methods=['POST'])
def text(id):
    params = {
        "apiKey": apikey
    }
    url = f"https://api.spoonacular.com/recipes/{id}/information"
    r = requests.get(url, params=params)
    if r.status_code == 200:
        json_recipe = json.loads(r.content)
        ingredients = json_recipe['extendedIngredients']
        title = json_recipe['title']
    else:
        return "error"

    all_ingredients = []

    for ingredient in ingredients:
        amount = ingredient['amount']
        measurement = ingredient['measures']['us']['unitShort']
        name = ingredient['name']
        all_ingredients.append(f"{amount} {measurement} {name}")

    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    msg_txt = "Ingredients for {}:\n{}".format(title, '\n'.join(all_ingredients))

    message = client.messages.create(
        body= msg_txt,
        from_=os.getenv("TWILIO_NUMBER"),
        to=f'+1{request.form.get("phone_number")}'
    )

    return redirect(url_for('display_single_recipe', id=id))    
    