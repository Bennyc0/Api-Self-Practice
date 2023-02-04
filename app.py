from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search-result", methods=['GET', 'POST'])
def search_result():
    search_name = request.form["input"].lower()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_name}")
    data = response.json()

    type_list = []
    ability_list = []
    advantage_list = []
    weakness_list = []

    pkmn_type in data['types']
    print(pkmn_type)
    type_list = type_list.append(pkmn_type['type']['name'])

#[{'ability': {'name': 'overgrow', 'url': 'https://pokeapi.co/api/v2/ability/65/'}, 'is_hidden': False, 'slot': 1}, {'ability': {'name': 'chlorophyll', 'url': 'https://pokeapi.co/api/v2/ability/34/'}, 'is_hidden': True, 'slot': 3}]

    for ability in data['abilities']:
        ability_list = ability_list.append(ability['name'])

    result = {
        "Name" : data['name'].capitalize(),
        "Pokedex ID" : data['id'],
        # "Types" : data['types'],
        # "Abilities" : data['abilities'],
        "Types" : type_list,
        # "Abilities": ability_list
        # "Advantages" : data['types']['url']['damage_relations']['double_damage_to'],
        # "Weaknesses" : data['types']['url']['damage_relations']['double_damage_from']
    }

    return render_template("index.html", response=result)

print("Code is Working")

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port='9000')