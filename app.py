# Use command '$ pip freeze > requirements.txt' to add packages to dependencies
import requests
import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from pymongo import MongoClient

app = Flask(__name__)
app.run(debug=True)

def get_table():
    client = MongoClient(os.getenv('CONNECTION_STRING'))
    db = client['NFL-Players']
    return db['Active NFL Players']


def get_players():
    try:
        load_dotenv()   
        url = 'https://api.sportsdata.io/v3/nfl/stats/json/FantasyPlayers'
        response = requests.get(url, headers={"Ocp-Apim-Subscription-Key": os.getenv('API_KEY')})
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        return response.json()
    except (KeyError, TypeError, ValueError):
        return None


@app.route("/")
def index():
    active_players = get_players()
    active_players_table = get_table()
    print(active_players_table.find())
    return render_template("index.html", active_players=active_players)

@app.route("/filter")
def filter():
    return redirect("/")



    

