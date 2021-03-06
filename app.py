from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json
import time
from twilio.rest import Client

# Spoonacular
apikey = os.getenv("API_KEY")


app = Flask(__name__, static_url_path='')

# Home page showing random recipes
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




# Results page for a recipe search
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

# Displays a single recipe with instructions
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

    for ingredient in ingredients:
        ingredient['amount'] = str(ingredient['amount']).rstrip('.0')
        ingredient['amount'] = str(ingredient['amount']).strip('0')

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


# Twilio route

# Sends a text message with a grocery list 
@app.route('/<id>/text', methods=['POST'])
def text(id):
    # Twilio Setup
    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")

    client = Client(account_sid, auth_token)

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
        amount = str(ingredient['amount']).rstrip('.0')
        amount = str(ingredient['amount']).strip('0')
        measurement = ingredient['measures']['us']['unitShort']
        name = ingredient['name']
        all_ingredients.append(f"{amount} {measurement} {name}")

    msg_txt = "Ingredients for {}:\n{}".format(title, '\n'.join(all_ingredients))

    message = client.messages.create(
        body= msg_txt,
        from_=twilio_number,
        to=f'+1{request.form.get("phone_number")}'
    )

    return redirect(url_for('display_single_recipe', id=id))    
    