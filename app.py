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


    search_term = request.args.get('user_input')


    params = {
        'query': search_term,
        'apiKey': apikey,
        'number': 3
    }

    


    r = requests.get("https://api.spoonacular.com/recipes/search", params=params)
    if r.status_code == 200:
        json_recipes = json.loads(r.content)
        recipes = json_recipes['results']
        return render_template('index.html', recipes=recipes)


    # "Welcome page"
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    
    