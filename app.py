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
        weakness_list := [],
        immunity_list := []]

    # Pokemon Type
    for pkmn_type in data['types']:
        type_list.append(pkmn_type['type']['name'].capitalize())

    # Pokemon Abilties
    for pkmn_abilities in data['abilities']:
        ability_list.append(pkmn_abilities['ability']['name'].capitalize())

    # Pokemon Image
    normal_variant = data['sprites']['other']['official-artwork']['front_default']
    shiny_variant = data['sprites']['other']['official-artwork']['front_shiny']

    # Pokemon Individual Type Damage Relations
    for searching_damage_relations in data['types']:
        response = requests.get(f"https://pokeapi.co/api/v2/type/{searching_damage_relations['type']['name']}").json()
        types = response['damage_relations']

        for weak_to in types['double_damage_from']:
            weakness_list.append(weak_to['name'].capitalize())

        for immune_to in types['no_damage_from']:
            immunity_list.append(immune_to['name'].capitalize())

    # Put Information Together
    pkmn_info = {
        "Name" : data['name'].capitalize(),
        "Pokedex ID" : str(data['id']),
        "Types" : ", ".join(type_list),
        "Abilities": ", ".join(ability_list),
        "Weak to" : ", ".join(weakness_list),
    }

    # Removing Pokedex ID For Special Forms
    if int(pkmn_info.get("Pokedex ID")) > 1008:
        pkmn_info.update({"Pokedex ID": "Unavailable"})

    # Adding Immunity List
    if len(immunity_list) > 0:
        pkmn_info.update({"Immune to": immunity_list})

    # Images
    pkmn_images = [normal_variant, shiny_variant]

    # Types Text Color Index
    type_color_index = {
        "Normal": "#A8A77A",
        "Fire": "#EE8130",
        "Water": "#6390F0",
        "Electric": "#F7D02C",
        "Grass": "#7AC74C",
        "Ice": "#96D9D6",
        "Fighting": "#C22E28",
        "Poison": "#A33EA1",
        "Ground": "#E2BF65",
        "Flying": "#A98FF3",
        "Psychic": "#F95587",
        "Bug": "#A6B91A",
        "Rock": "#B6A136",
        "Ghost": "#735797",
        "Dragon": "#6F35FC",
        "Dark": "#705746",
        "Steel": "#B7B7CE",
        "Fairy": "#D685AD"
    }

    # Text Color Empty Lists
    pkmn_type_colors = []
    pkmn_weak_colors = []
    pkmn_immune_colors = []

    for pkmn_type in pkmn_info["Types"]:
        pkmn_type_colors.append(type_color_index.get(pkmn_type))



    return render_template("index.html", pkmn_info=pkmn_info, pkmn_images=pkmn_images, type_colors=type_color_index)

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port='9000')