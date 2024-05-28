import streamlit as st
import hashlib
import json
import sqlite3
import os
import base64
from PIL import Image
from io import BytesIO

# Initialize SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                     email TEXT PRIMARY KEY,
                     password TEXT
                   )''')

# Create characters table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS characters (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     email TEXT,
                     name TEXT,
                     age INTEGER,
                     gender TEXT,
                     race TEXT,
                     body_type TEXT,
                     eye_color TEXT,
                     hair_color TEXT,
                     skin_color TEXT,
                     skin_condition TEXT,
                     characteristics TEXT,
                     perks TEXT,
                     flaws TEXT,
                     special_traits TEXT,
                     image TEXT,
                     FOREIGN KEY (email) REFERENCES users (email)
                   )''')
conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user data from the SQLite database
def load_user_data(email):
    cursor.execute('SELECT password FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    return user

# Function to save user data to the SQLite database
def save_user_data(email, password):
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hash_password(password)))
    conn.commit()

# Function to handle user registration
def register_user(email, password):
    if load_user_data(email):
        st.error("Email already registered")
        return

    save_user_data(email, password)
    st.success(f"Registered user with email: {email}")
    st.session_state.logged_in = True
    st.session_state.email = email
    st.session_state.characters = []

# Function to handle user login
def login_user(email, password):
    user = load_user_data(email)
    if not user:
        st.error("Email not registered")
        return

    hashed_password = hash_password(password)
    if user[0] == hashed_password:
        st.success(f"Logged in user with email: {email}")
        st.session_state.logged_in = True
        st.session_state.email = email
        st.session_state.characters = load_user_characters(email)
    else:
        st.error("Incorrect password")

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.characters = []
    st.session_state.email = None
    st.success("Logged out successfully")

# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    img = Image.open(image)
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to convert base64 to image
def base64_to_image(base64_str):
    return Image.open(BytesIO(base64.b64decode(base64_str)))

# Function to save character data
def save_character_data(email, characters):
    cursor.execute('DELETE FROM characters WHERE email=?', (email,))
    for character in characters:
        cursor.execute('''INSERT INTO characters (email, name, age, gender, race, body_type, eye_color, hair_color, skin_color, skin_condition, characteristics, perks, flaws, special_traits, image) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (email, character['name'], character['age'], character['gender'], character['race'], character['body_type'], character['eye_color'], character['hair_color'], character['skin_color'], character['skin_condition'], character['characteristics'], character['perks'], character['flaws'], character['special_traits'], character['image']))
    conn.commit()

# Function to load user characters from the SQLite database
def load_user_characters(email):
    cursor.execute('SELECT name, age, gender, race, body_type, eye_color, hair_color, skin_color, skin_condition, characteristics, perks, flaws, special_traits, image FROM characters WHERE email=?', (email,))
    characters = cursor.fetchall()
    character_list = []
    for character in characters:
        character_data = {
            "name": character[0],
            "age": character[1],
            "gender": character[2],
            "race": character[3],
            "body_type": character[4],
            "eye_color": character[5],
            "hair_color": character[6],
            "skin_color": character[7],
            "skin_condition": character[8],
            "characteristics": character[9],
            "perks": character[10],
            "flaws": character[11],
            "special_traits": character[12],
            "image": character[13]
        }
        character_list.append(character_data)
    return character_list

# Function to create a new character
def create_character():
    st.title("Create New Character")
    st.subheader("Character Traits")

    # Input fields for character traits
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=200, value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    race = st.selectbox("Race", ["Human", "Elf", "Dwarf", "Orc", "Goblin", "Tiefling", "Half Elf", "Dragonborn", "Half Orc", "Other"])
    body_type = st.text_input("Body Type", "Enter body type here...")
    eye_color = st.color_picker("Eye Color", "#FFFFFF")  # Default color is white
    hair_color = st.color_picker("Hair Color", "#FFFFFF")  # Default color is white
    skin_color = st.color_picker("Skin Color", "#FFFFFF")  # Default color is white
    skin_condition = st.text_input("Skin Condition", "Enter skin condition here...")
    characteristics = st.text_area("Characteristics", "Enter characteristics here...")
    perks = st.text_area("Perks", "Enter perks here...")
    flaws = st.text_area("Flaws", "Enter flaws here...")
    special_traits = st.text_area("Special Traits", "Enter special traits here...")
    character_image = st.file_uploader("Upload Character Image", type=["jpg", "jpeg", "png"])

    if st.button("Create Character"):
        # Save character data to session state
        character_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "race": race,
            "body_type": body_type,
            "eye_color": eye_color,
            "hair_color": hair_color,
            "skin_color": skin_color,
            "skin_condition": skin_condition,
            "characteristics": characteristics,
            "perks": perks,
            "flaws": flaws,
            "special_traits": special_traits,
            "image": None
        }

        # Handle image upload
        if character_image:
            character_data["image"] = image_to_base64(character_image)

        st.session_state.characters.append(character_data)
        save_character_data(st.session_state.email, st.session_state.characters)
        st.success("Character created successfully")

# Function to edit an existing character
def edit_character():
    st.title("Edit Character")
    characters = [character["name"] for character in st.session_state.characters]
    selected_character = st.selectbox("Select Character to Edit", characters)
    selected_character_data = next(character for character in st.session_state.characters if character["name"] == selected_character)

    st.subheader("Edit Character Traits")
    selected_character_data["name"] = st.text_input("Name", selected_character_data["name"])
    selected_character_data["age"] = st.number_input("Age", min_value=0, max_value=200, value=selected_character_data["age"])
    selected_character_data["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(selected_character_data["gender"]))
    selected_character_data["race"] = st.selectbox("Race", ["Human", "Elf", "Dwarf", "Orc", "Goblin", "Tiefling", "Half Elf", "Dragonborn", "Half Orc", "Other"], index=["Human", "Elf", "Dwarf", "Orc", "Goblin", "Tiefling", "Half Elf", "Dragonborn", "Half Orc", "Other"].index(selected_character_data["race"]))
    selected_character_data["body_type"] = st.text_input("Body Type", selected_character_data["body_type"])
    selected_character_data["eye_color"] = st.color_picker("Eye Color", selected_character_data["eye_color"])
    selected_character_data["hair_color"] = st.color_picker("Hair Color", selected_character_data["hair_color"])
    selected_character_data["skin_color"] = st.color_picker("Skin Color", selected_character_data["skin_color"])
    selected_character_data["skin_condition"] = st.text_input("Skin Condition", selected_character_data["skin_condition"])
    selected_character_data["characteristics"] = st.text_area("Characteristics", selected_character_data["characteristics"])
    selected_character_data["perks"] = st.text_area("Perks", selected_character_data["perks"])
    selected_character_data["flaws"] = st.text_area("Flaws", selected_character_data["flaws"])
    selected_character_data["special_traits"] = st.text_area("Special Traits", selected_character_data["special_traits"])

    character_image = st.file_uploader("Upload Character Image", type=["jpg", "jpeg", "png"], key="edit_image")
    if character_image:
        selected_character_data["image"] = image_to_base64(character_image)

    if st.button("Save Changes"):
        save_character_data(st.session_state.email, st.session_state.characters)
        st.success("Character changes saved successfully")

# Function to load created characters
def load_characters():
    st.title("Load Characters")
    if st.session_state.characters:
        for character in st.session_state.characters:
            st.write(f"Name: {character['name']}")
            if character['image']:
                st.image(base64_to_image(character['image']), caption=character['name'], width=150)
            else:
                st.write("No image available for this character.")
    else:
        st.write("No characters created yet.")

# Main function
def main():
    # Display logo at the top of the app
    st.image("logo.jpeg", width=200)
    st.title("Character Logbook")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.title("Options")
        option = st.sidebar.selectbox("Choose an option", ("Create New Character", "Edit Character", "Load Characters", "Log Out"))

        if option == "Create New Character":
            create_character()
        elif option == "Edit Character":
            edit_character()
        elif option == "Load Characters":
            load_characters()
        elif option == "Log Out":
            logout()
    else:
        # Login or Register
        login_or_register = st.radio("Login or Register", ("Login", "Register"))
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button(login_or_register):
            st.session_state.email = email
            if login_or_register == "Login":
                login_user(email, password)
            else:
                register_user(email, password)

if __name__ == "__main__":
    main()
