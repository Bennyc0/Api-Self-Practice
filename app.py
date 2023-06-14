from flask import Flask, render_template, request, redirect, url_for
import requests
import database_functions as dbf

app = Flask(__name__)
current_user = ""
current_email = ""


# ---------- Functions ----------
def get_normal_sprites(loadout):
    normal_sprites = []

    for pokemon in loadout:
        search_name = pokemon.lower().replace(" ", "-")

        try:
            print(search_name)
            if search_name != "empty":
                data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_name}").json()
                sprite = data['sprites']['other']['official-artwork']['front_default']
                normal_sprites.append(sprite)
                print(sprite)
            else:
                normal_sprites.append("/static/images/Blank.jpeg")
        except:
            normal_sprites.append("/static/images/Blank.jpeg")
    
    return normal_sprites


# ---------- Homepage ----------
# Index/Home
@app.route("/")
def home():
    global current_user

    welcome_message = ""

    if current_user != "":
        welcome_message = f"Hello there {current_user}! Welcome to Simple Pokedex"

    return render_template("home.html", current_user=current_user, welcome_message=welcome_message)


# ---------- Login/Signup ----------
# Login
@app.route("/login")
def login():
    return render_template("login.html")

# Sign Up
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Verify User
@app.route("/verify-user", methods=['GET', 'POST'])
def verify_user():
    global current_user
    global current_email

    username = ""
    email = request.form['email']
    password = request.form['password']

    current_user = dbf.verify_user(email, password)

    if current_user != "":
        current_email = email

        return redirect(url_for('home'))
    else:
        return render_template('login.html', message='Invalid Gmail or Password, Please Try Again')

# Store User
@app.route('/store-user', methods=['GET', 'POST'])
def store_user():
    global current_user
    global current_email

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if dbf.get_user_rowid(email) == "":
        dbf.signup_user(username, email, password)

        current_user = username
        current_email = email

        return redirect(url_for('home'))

    else:
        return render_template('login.html', message="Email Already In Use, Log In Instead?")

# Log Out
@app.route('/logout')
def logout():
    global current_user
    global current_email

    current_user = ""
    current_email = ""

    return render_template('login.html', message='Successfully Logged Out!')


# ---------- Loadouts ----------
# Loadouts 
@app.route("/loadouts", methods=['GET', 'POST'])
def loadouts():
    global current_user
    global current_email

    if request.method == 'GET' or request.method == 'POST':
        user_rowid = dbf.get_user_rowid(current_email)
        user_loadouts = dbf.find_user_loadouts(user_rowid)

    if current_user != "":
        return render_template('loadouts.html', current_user=current_user, user_loadouts=user_loadouts)
    else:
        return redirect(url_for('home'))

# New Loadout
@app.route("/new-loadout", methods=['POST'])
def new_loadout():
    global current_email

    loadout = [
        request.form['slot_1'].title().strip(),
        request.form['slot_2'].title().strip(),
        request.form['slot_3'].title().strip(),
        request.form['slot_4'].title().strip(),
        request.form['slot_5'].title().strip(),
        request.form['slot_6'].title().strip()
    ]

    normal_sprites = get_normal_sprites(loadout)

    dbf.save_loadout(current_email, loadout, normal_sprites)

    return redirect(url_for('loadouts'))

# Edit Loadout
@app.route("/edit-loadout/<rowid>")
def edit_loadout(rowid):
    row_information = dbf.find_row(rowid)

    return render_template('edit-loadout.html', row_information=row_information[0])

# Process Edit
@app.route("/process-edit/<rowid>", methods=['POST'])
def process_edit(rowid):
    loadout = [
        request.form['slot_1'].title().strip(),
        request.form['slot_2'].title().strip(),
        request.form['slot_3'].title().strip(),
        request.form['slot_4'].title().strip(),
        request.form['slot_5'].title().strip(),
        request.form['slot_6'].title().strip()
    ]

    normal_sprites = get_normal_sprites(loadout)

    dbf.update_loadout(rowid, loadout, normal_sprites)

    return redirect(url_for('loadouts'))

# Delete Loadout
@app.route("/delete-loadout/<rowid>")
def delete_loadout(rowid):
    dbf.delete_loadout(rowid)

    return redirect(url_for('loadouts'))

# ---------- Search Result ----------
@app.route("/search-result", methods=['GET', 'POST'])
def search_result():
    search_name = request.form["input"].lower().strip()
    search_name = search_name.replace(" ", "-")

    try:
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_name}").json()
    except :
        return render_template('search-result.html', message="No Search Results Found, Check Your Spelling")

    # Empty Lists
    lists = [
        type_list := [],
        ability_list := [],
        uneffective_list := [],
        weakness_list := [],
        immunity_list := []
    ]

    # Empty Lists Used For Processing
    hidden_lists = [
        temp_weakness_list := [],
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
            
    # Removing Dashes in Certain Pokemon Names
    pkmn_name = data['name'].title().replace("-", " ")

    # Put Information Together
    pkmn_info = {
        "Name" : pkmn_name,
        "Pokedex ID" : str(data['id']),
        "Types" : type_list,
        "Abilities": ", ".join(ability_list),
        "Weak to" : weakness_list,
    }

    # Removing Pokedex ID For Special Forms
    if int(pkmn_info.get("Pokedex ID")) > 1010:
        pkmn_info.update({"Pokedex ID": "Unavailable"})

    # Adding Immunity List
    if len(immunity_list) > 0:
        pkmn_info.update({"Immune to": immunity_list})

    # Pokemon Images
    normal_sprite = data['sprites']['other']['official-artwork']['front_default']
    shiny_sprite = data['sprites']['other']['official-artwork']['front_shiny']

    return render_template("search-result.html", pkmn_info=pkmn_info, normal_sprite=normal_sprite, shiny_sprite=shiny_sprite)

if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')