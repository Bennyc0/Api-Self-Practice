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

    result = cursor.execute('SELECT rowid, * FROM loadouts WHERE user_id = ?', (rowid,))

    loadouts = []

    for item in result:
        instance = {
            "rowid": item[0],

            "slot_1": item[2],
            "sprite_1": item[3],

            "slot_2": item[4],
            "sprite_2": item[5],

            "slot_3": item[6],
            "sprite_3": item[7],

            "slot_4": item[8],
            "sprite_4": item[9],

            "slot_5": item[10],
            "sprite_5": item[11],

            "slot_6": item[12],
            "sprite_6": item[13],
        }

        loadouts.append(instance)

    connect.close()

    return loadouts

# Uses rowid to Find Specific Row
def find_row(rowid):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    result = cursor.execute('SELECT rowid, * FROM loadouts WHERE rowid = ?', (rowid,))

    loadouts = []

    for item in result:
        instance = {
            "rowid": item[0],

            "slot_1": item[2],
            "sprite_1": item[3],

            "slot_2": item[4],
            "sprite_2": item[5],

            "slot_3": item[6],
            "sprite_3": item[7],

            "slot_4": item[8],
            "sprite_4": item[9],

            "slot_5": item[10],
            "sprite_5": item[11],

            "slot_6": item[12],
            "sprite_6": item[13],
        }

        loadouts.append(instance)

    connect.close()

    return loadouts

# Save Loadout
def save_loadout(email, loadout, normal_sprites):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    user_rowid = get_user_rowid(email)

    # Slots Are Pokemon Names, Sprites Are That Pokemon's Sprite
    cursor.execute('INSERT INTO loadouts(user_id, slot_1, sprite_1, slot_2, sprite_2, slot_3, sprite_3, slot_4, sprite_4, slot_5, sprite_5, slot_6, sprite_6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_rowid, loadout[0], normal_sprites[0], loadout[1], normal_sprites[1], loadout[2], normal_sprites[2], loadout[3], normal_sprites[3], loadout[4], normal_sprites[4], loadout[5], normal_sprites[5],))

    connect.commit()
    connect.close()

# Update Loadout
def update_loadout(rowid, loadout, normal_sprites):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    # Slots Are Pokemon Names, Sprites Are That Pokemon's Sprite
    cursor.execute('UPDATE loadouts SET slot_1 = ?, sprite_1 = ?, slot_2 = ?, sprite_2 = ?, slot_3 = ?, sprite_3 = ?, slot_4 = ?, sprite_4 = ?, slot_5 = ?, sprite_5 = ?, slot_6 = ?, sprite_6 = ? WHERE rowid = ?', (loadout[0], normal_sprites[0], loadout[1], normal_sprites[1], loadout[2], normal_sprites[2], loadout[3], normal_sprites[3], loadout[4], normal_sprites[4], loadout[5], normal_sprites[5], rowid,))

    connect.commit()
    connect.close() 

# Delete Loadout
def delete_loadout(rowid):
    connect = sqlite3.connect(database_link)
    cursor = connect.cursor()

    cursor.execute('DELETE FROM loadouts WHERE rowid = ?', (rowid,))
    
    connect.commit()
    connect.close()
