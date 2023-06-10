import sqlite3

database_link = "./static/data/database.db"

# ---------- Login/Signup ----------
# Verify User
def verify_user(email, password):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    result = cursor.execute('SELECT * FROM userbase WHERE email = ? AND password = ?', (email, password,))
        
    information = {
        "username": ""
    }
    
    for item in result:
        information = {
            "username": item[0]
        }

    connect.close()
    return information['username']

# Sign Up
def signup_user(username, email, password):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    cursor.execute('INSERT INTO userbase(username, email, password) VALUES (?, ?, ?)', (username, email, password,))

    connect.commit()
    connect.close()


# ---------- Get User ----------
# Finds User ID Associated With Email
# Can Also Be Used To Prevent Duplicate Email (If Nothing Is Found, Returns Blank, Meaning Email Not In Use Yet)
def get_user_rowid(email):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    result = cursor.execute('SELECT rowid FROM userbase WHERE email = ?', (email,))
        
    information = {
        "rowid": ""
    }
    
    for item in result:
        information = {
            "rowid": item[0]
        }

    connect.close()
    return information['rowid']


# ---------- Loadouts ----------
# Uses User ID To Find Saved Loadouts
def find_user_loadouts(rowid):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    result = cursor.execute('SELECT * FROM loadouts WHERE rowid = ?', (rowid,))
    
    loadouts = []

    for item in result:
        information = {
            # item[0] returns rowid
            "slot 1": item[1],
            "slot 2": item[2],
            "slot 3": item[3],
            "slot 4": item[4],
            "slot 5": item[5],
            "slot 6": item[6]
        }

        loadouts.append(information)

    connect.close()

    return loadouts

def save_loadout(email, loadout_list, normal_sprites):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    user_rowid = get_user_rowid(email)

    # Slots Are Pokemon Names, Sprites Are That Pokemon's Sprite
    cursor.execute('INSERT INTO loadouts(user_id, slot_1, sprite_1, slot_2, sprite_2, slot_3, sprite_3, slot_4, sprite_4, slot_5, sprite_5, slot_6, sprite_6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_rowid, loadout_list[0], normal_sprites[0], loadout_list[1], normal_sprites[1], loadout_list[2], normal_sprites[2], loadout_list[3], normal_sprites[3], loadout_list[4], normal_sprites[4], loadout_list[5], normal_sprites[5],))

    connect.commit()
    connect.close()
