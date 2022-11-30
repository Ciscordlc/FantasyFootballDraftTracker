import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()   

def get_players():
    try:
        url = 'https://api.sportsdata.io/v3/nfl/stats/json/FantasyPlayers'
        response = requests.get(url, headers={"Ocp-Apim-Subscription-Key": os.getenv('API_KEY')})
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        players = response.json()
        player_keys = list(players[0].keys())
        wanted_keys = ['PlayerID', 'Name', 'Team', 'Positin', 'ByeWeek']
        unwanted_keys = [key for key in player_keys if key not in wanted_keys]
        for player in players:
            for key in unwanted_keys:
                player.pop(key)
            player['Drafted'] = False
        return players 
    except (KeyError, TypeError, ValueError):
        return None

def populate_db():
    client = MongoClient(os.getenv('CONNECTION_STRING'))
    db = client['NFL-Players']
    db['Active NFL Players'].drop()
    nfl_players_table = db['Active NFL Players']
    active_players = get_players()

    nfl_players_table.insert_many(active_players)

if __name__ == '__main__':
    populate_db()