import streamlit as st
import hashlib
import json
import os
import base64
import requests
from PIL import Image
from io import BytesIO

# GitHub-Informationen
GITHUB_TOKEN = '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'  # Ersetze durch deinen tatsächlichen Token
REPO_OWNER = 'Quickrice'  # Ersetze durch deinen GitHub-Benutzernamen
REPO_NAME = 'Hello_Sanguinis'  # Ersetze durch den Namen deines Repositories
FILE_PATH = 'user_data.json'  # Der Pfad zur Datei im Repository

# Funktion zum Hashen von Passwörtern
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funktion zum Laden von Benutzerdaten aus der JSON-Datei auf GitHub
def load_user_data():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_content = base64.b64decode(response.json()['content']).decode()
        return json.loads(file_content)
    elif response.status_code == 404:
        return {}  # Datei nicht gefunden, leere Daten zurückgeben
    else:
        st.error("Fehler beim Laden der Benutzerdaten von GitHub")
        return {}

# Funktion zum Speichern von Benutzerdaten in die JSON-Datei auf GitHub
def save_user_data(user_data):
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    data = {
        'message': 'Automated upload of user data',
        'content': base64.b64encode(json.dumps(user_data).encode()).decode(),
        'branch': 'main'  # oder dein gewünschter Branch
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201 or response.status_code == 200:
        st.success("Benutzerdaten erfolgreich gespeichert")
    else:
        st.error("Fehler beim Speichern der Benutzerdaten auf GitHub")

# Funktion zur Benutzerregistrierung
def register_user(email, password):
    user_data = load_user_data()
    if email in user_data:
        st.error("Email bereits registriert")
        return

    hashed_password = hash_password(password)
    user_data[email] = {"email": email, "password": hashed_password, "characters": []}
    save_user_data(user_data)
    st.success(f"Benutzer mit Email {email} registriert")
    st.session_state.logged_in = True
    st.session_state.characters = []
    st.session_state.email = email

# Funktion zur Benutzeranmeldung
def login_user(email, password):
    user_data = load_user_data()
    if email not in user_data:
        st.error("Email nicht registriert")
        return

    hashed_password = hash_password(password)
    if user_data[email]["password"] == hashed_password:
        st.success(f"Benutzer mit Email {email} angemeldet")
        st.session_state.logged_in = True
        st.session_state.characters = user_data[email].get("characters", [])
        st.session_state.email = email
    else:
        st.error("Falsches Passwort")

# Funktion zum Abmelden
def logout():
    st.session_state.logged_in = False
    st.session_state.characters = []
    st.session_state.email = None
    st.success("Erfolgreich abgemeldet")

# Funktion zum Konvertieren von Bildern in Base64
def image_to_base64(image):
    buffered = BytesIO()
    img = Image.open(image)
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Funktion zum Konvertieren von Base64 in Bilder
def base64_to_image(base64_str):
    return Image.open(BytesIO(base64.b64decode(base64_str)))

# Funktion zum Erstellen eines neuen Charakters
def create_character():
    st.title("Neuen Charakter erstellen")
    st.subheader("Charaktereigenschaften")

    # Eingabefelder für Charaktereigenschaften
    name = st.text_input("Name")
    age = st.number_input("Alter", min_value=0, max_value=200, value=0)
    gender = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Andere"])
    race = st.selectbox("Rasse", ["Mensch", "Elf", "Zwerg", "Ork", "Goblin", "Tiefling", "Halbelf", "Drachengeborener", "Halbork", "Andere"])
    body_type = st.text_input("Körperbau", "Körperbau hier eingeben...")
    eye_color = st.color_picker("Augenfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    hair_color = st.color_picker("Haarfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    skin_color = st.color_picker("Hautfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    skin_condition = st.text_input("Hautzustand", "Hautzustand hier eingeben...")
    characteristics = st.text_area("Charakteristika", "Charakteristika hier eingeben...")
    perks = st.text_area("Vorteile", "Vorteile hier eingeben...")
    flaws = st.text_area("Fehler", "Fehler hier eingeben...")
    special_traits = st.text_area("Besondere Merkmale", "Besondere Merkmale hier eingeben...")
    character_image = st.file_uploader("Charakterbild hochladen", type=["jpg", "jpeg", "png"])

    if st.button("Charakter erstellen"):
        # Charakterdaten in Session State speichern
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

        # Bild hochladen
        if character_image:
            character_data["image"] = image_to_base64(character_image)

        st.session_state.characters.append(character_data)
        save_character_data(st.session_state.characters)
        st.success("Charakter erfolgreich erstellt")

# Funktion zum Bearbeiten eines vorhandenen Charakters
def edit_character():
    st.title("Charakter bearbeiten")
    characters = [character["name"] for character in st.session_state.characters]
    selected_character = st.selectbox("Zu bearbeitenden Charakter auswählen", characters)
    selected_character_data = next(character for character in st.session_state.characters if character["name"] == selected_character)

    st.subheader("Charaktereigenschaften bearbeiten")
    selected_character_data["name"] = st.text_input("Name", selected_character_data["name"])
    selected_character_data["age"] = st.number_input("Alter", min_value=0, max_value=200, value=selected_character_data["age"])
    selected_character_data["gender"] = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Andere"], index=["Männlich", "Weiblich", "Andere"].index(selected_character_data["gender"]))
    selected_character_data["race"] = st.selectbox("Rasse", ["Mensch", "Elf", "Zwerg", "Ork", "Goblin", "Tiefling", "Halbelf", "Drachengeborener", "Halbork", "Andere"], index=["Mensch", "Elf", "Zwerg", "Ork", "Goblin", "Tiefling", "Halbelf", "Drachengeborener", "Halbork", "Andere"].index(selected_character_data["race"]))
    selected_character_data["body_type"] = st.text_input("Körperbau", selected_character_data["body_type"])
    selected_character_data["eye_color"] = st.color_picker("Augenfarbe", selected_character_data["eye_color"])
    selected_character_data["hair_color"] = st.color_picker("Haarfarbe", selected_character_data["hair_color"])
    selected_character_data["skin_color"] = st.color_picker("Hautfarbe", selected_character_data["skin_color"])
    selected_character_data["skin_condition"] = st.text_input("Hautzustand", selected_character_data["skin_condition"])
    selected_character_data["characteristics"] = st.text_area("Charakteristika", selected_character_data["characteristics"])
    selected_character_data["perks"] = st.text_area("Vorteile", selected_character_data["perks"])
    selected_character_data["flaws"] = st.text_area("Fehler", selected_character_data["flaws"])
    selected_character_data["special_traits"] = st.text_area("Besondere Merkmale", selected_character_data["special_traits"])

    character_image = st.file_uploader("Charakterbild hochladen", type=["jpg", "jpeg", "png"], key="edit_image")
    if character_image:
        selected_character_data["image"] = image_to_base64(character_image)

    if st.button("Änderungen speichern"):
        save_character_data(st.session_state.characters)
        st.success("Charakteränderungen erfolgreich gespeichert")

# Funktion zum Laden der erstellten Charaktere
def load_characters():
    st.title("Charaktere laden")
    if st.session_state.characters:
        for character in st.session_state.characters:
            st.write(f"Name: {character['name']}")
            if character['image']:
                st.image(base64_to_image(character['image']), caption=character['name'], width=150)
            else:
                st.write("Kein Bild für diesen Charakter verfügbar.")
    else:
        st.write("Noch keine Charaktere erstellt.")

# Funktion zum Speichern der Charakterdaten
def save_character_data(characters):
    user_data = load_user_data()
    user_data[st.session_state.email]["characters"] = characters
    save_user_data(user_data)

# Hauptfunktion
def main():
    # Logo oben in der App anzeigen
    st.image("logo.jpeg", width=200)
    st.title("Charakter-Logbuch")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.title("Optionen")
        option = st.sidebar.selectbox("Option auswählen", ("Neuen Charakter erstellen", "Charakter bearbeiten", "Charaktere laden", "Abmelden"))

        if option == "Neuen Charakter erstellen":
            create_character()
        elif option == "Charakter bearbeiten":
            edit_character()
        elif option == "Charaktere laden":
            load_characters()
        elif option == "Abmelden":
            logout()
    else:
        # Login oder Registrierung
        login_or_register = st.radio("Login oder Registrierung", ("Login", "Registrieren"))
        email = st.text_input("Email")
        password = st.text_input("Passwort", type="password")

        if st.button(login_or_register):
            st.session_state.email = email
            if login_or_register == "Login":
                login_user(email, password)
            else:
                register_user(email, password)

if __name__ == "__main__":
    main()
