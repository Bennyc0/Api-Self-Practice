from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search-result", methods=['GET', 'POST'])
def search_result():
    search_name = request.form["input"].lower().strip()

    try:
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_name}").json()
        testing = data['name']
    except :
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/bulbasaur").json()

    # Empty Lists
    lists = [
        type_list := [],
        ability_list := [],
        uneffective_list := [],
        temp_weakness_list := [],
        weakness_list := [],
        immunity_list := []
    ]

    hidden_lists = [
        advantage_list := []
    ]

    # Pokemon Type
    for pkmn_type in data['types']:
        type_list.append(pkmn_type['type']['name'].capitalize())

    # Pokemon Abilties
    for pkmn_abilities in data['abilities']:
        ability_list.append(pkmn_abilities['ability']['name'].capitalize())

    # Pokemon Individual Type Damage Relations
    for searching_damage_relations in data['types']:
        response = requests.get(f"https://pokeapi.co/api/v2/type/{searching_damage_relations['type']['name']}").json()
        types = response['damage_relations']

        for weak_to in types['double_damage_from']:
            if weak_to['name'].capitalize() not in weakness_list:
                temp_weakness_list.append(weak_to['name'].capitalize())

        for immune_to in types['no_damage_from']:
            immunity_list.append(immune_to['name'].capitalize())

        # Hidden Lists (Used to netraulize/remove types weaknesses)
        for strong_to in types['double_damage_to']:
            if strong_to['name'].capitalize() not in advantage_list:
                advantage_list.append(strong_to['name'].capitalize())

        for half_from in types['half_damage_from']:
            if half_from['name'].capitalize() not in advantage_list:
                advantage_list.append(half_from['name'].capitalize())

    # Neutralizing/Removing Type Weaknesses
    for weakness in temp_weakness_list:
        if not (weakness in type_list or weakness in immunity_list or weakness in advantage_list or weakness in weakness_list):
            weakness_list.append(weakness)
            

    # Put Information Together
    pkmn_info = {
        "Name" : data['name'].capitalize(),
        "Pokedex ID" : str(data['id']),
        "Types" : type_list,
        "Abilities": ", ".join(ability_list),
        "Weak to" : ", ".join(weakness_list),
    }

    # Removing Pokedex ID For Special Forms
    if int(pkmn_info.get("Pokedex ID")) > 1008:
        pkmn_info.update({"Pokedex ID": "Unavailable"})

    # Adding Immunity List
    if len(immunity_list) > 0:
        pkmn_info.update({"Immune to": ", ".join(immunity_list)})

    # Pokemon Images
    normal_sprite = data['sprites']['other']['official-artwork']['front_default']
    shiny_sprite = data['sprites']['other']['official-artwork']['front_shiny']

    # Pokemon Type Colors
    type_colors = {
        "Normal": "A8A77A",
        "Fire": "EE8130",
        "Water": "6390F0",
        "Electric": "F7D02C",
        "Grass": "7AC74C",
        "Ice": "96D9D6",
        "Fighting": "C22E28",
        "Poison": "A33EA1",
        "Ground": "E2BF65",
        "Flying": "A98FF3",
        "Psychic": "F95587",
        "Bug": "A6B91A",
        "Rock": "B6A136",
        "Ghost": "735797",
        "Dragon": "6F35FC",
        "Dark": "05746",
        "Steel": "B7B7CE",
        "Fairy": "D685AD" 
    }

    return render_template("search-result.html", pkmn_info=pkmn_info, normal_sprite=normal_sprite, shiny_sprite=shiny_sprite, type_colors=type_colors)

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')