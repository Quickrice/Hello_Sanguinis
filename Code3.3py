import streamlit as st
import hashlib
import json
import os
import base64
from PIL import Image
from io import BytesIO

# File to store user data
USER_DATA_FILE = "user_data.json"

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r") as file:
                data = json.load(file)
                print(f"Loaded user data: {data}")  # Debug statement
                return data
        except json.JSONDecodeError:
            print("JSONDecodeError: The JSON file is empty or contains invalid data.")
            return {}
    return {}

# Function to save user data to the JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file)
        print(f"Saved user data: {user_data}")  # Debug statement

# Function to handle user registration
def register_user(email, password):
    user_data = load_user_data()
    if email in user_data:
        st.error("Email already registered")
        return

    hashed_password = hash_password(password)
    user_data[email] = {"email": email, "password": hashed_password, "characters": []}
    save_user_data(user_data)
    st.success(f"Registered user with email: {email}")
    st.session_state.logged_in = True
    st.session_state.characters = []
    st.session_state.email = email  # Ensure email is stored in session state

# Function to handle user login
def login_user(email, password):
    user_data = load_user_data()
    st.write(f"Loaded user data: {user_data}")  # Debug statement
    if email not in user_data:
        st.error("Email not registered")
        return

    hashed_password = hash_password(password)
    st.write(f"Hashed password: {hashed_password}")  # Debug statement
    if user_data[email]["password"] == hashed_password:
        st.success(f"Logged in user with email: {email}")
        st.session_state.logged_in = True
        st.session_state.characters = user_data[email].get("characters", [])
        st.session_state.email = email  # Ensure email is stored in session state
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
        save_character_data(st.session_state.characters)
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
        save_character_data(st.session_state.characters)
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

# Function to save character data
def save_character_data(characters):
    user_data = load_user_data()
    user_data[st.session_state.email]["characters"] = characters
    save_user_data(user_data)

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
