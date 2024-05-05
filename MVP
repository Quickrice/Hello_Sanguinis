import streamlit as st

# Function to handle user registration
def register_user(email):
    # Dummy implementation for demonstration
    st.success(f"Registered user with email: {email}")
    st.session_state.logged_in = True
    st.session_state.characters = []

# Function to handle user login
def login_user(email):
    # Dummy implementation for demonstration
    st.success(f"Logged in user with email: {email}")
    st.session_state.logged_in = True
    if "characters" not in st.session_state:
        st.session_state.characters = []

# Function to create a new character
def create_character():
    st.title("Create New Character")
    st.subheader("Character Traits")

    # Input fields for character traits
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=200, value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    race = st.selectbox("Race", ["Human", "Elf", "Dwarf", "Orc", "Goblin", "Other"])
    body_type = st.text_input("Body Type", "Enter body type here...")
    eye_color = st.color_picker("Eye Color", "#FFFFFF")  # Default color is white
    hair_color = st.color_picker("Hair Color", "#FFFFFF")  # Default color is white
    characteristics = st.text_area("Characteristics", "Enter characteristics here...")
    perks = st.text_area("Perks", "Enter perks here...")
    flaws = st.text_area("Flaws", "Enter flaws here...")
    special_traits = st.text_area("Special Traits", "Enter special traits here...")

    # Image upload option for character picture
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
            "characteristics": characteristics,
            "perks": perks,
            "flaws": flaws,
            "special_traits": special_traits,
            "image": character_image
        }
        st.session_state.characters.append(character_data)
        st.success("Character created successfully")

# Function to edit an existing character
def edit_character():
    st.title("Edit Character")
    characters = [character["name"] for character in st.session_state.characters]
    selected_character = st.selectbox("Select Character to Edit", characters)
    selected_character_data = [character for character in st.session_state.characters if character["name"] == selected_character][0]

    st.subheader("Edit Character Traits")

    # Input fields for character traits
    selected_character_data["name"] = st.text_input("Name", selected_character_data["name"])
    selected_character_data["age"] = st.number_input("Age", min_value=0, max_value=200, value=selected_character_data["age"])
    selected_character_data["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(selected_character_data["gender"]))
    selected_character_data["race"] = st.selectbox("Race", ["Human", "Elf", "Dwarf", "Orc", "Goblin", "Other"], index=["Human", "Elf", "Dwarf", "Orc", "Goblin", "Other"].index(selected_character_data["race"]))
    selected_character_data["body_type"] = st.text_input("Body Type", selected_character_data["body_type"])
    selected_character_data["eye_color"] = st.color_picker("Eye Color", selected_character_data["eye_color"])  
    selected_character_data["hair_color"] = st.color_picker("Hair Color", selected_character_data["hair_color"])
    selected_character_data["characteristics"] = st.text_area("Characteristics", selected_character_data["characteristics"])
    selected_character_data["perks"] = st.text_area("Perks", selected_character_data["perks"])
    selected_character_data["flaws"] = st.text_area("Flaws", selected_character_data["flaws"])
    selected_character_data["special_traits"] = st.text_area("Special Traits", selected_character_data["special_traits"])

    # Image upload option for character picture
    character_image = st.file_uploader("Upload Character Image", type=["jpg", "jpeg", "png"], key="edit_image")
    if character_image:
        selected_character_data["image"] = character_image

    if st.button("Save Changes"):
        st.success("Character changes saved successfully")

# Function to load created characters
def load_characters():
    st.title("Load Characters")
    if st.session_state.characters:
        for character in st.session_state.characters:
            st.write(f"Name: {character['name']}")
            if character['image']:
                st.image(character['image'], caption=character['name'], width=150)
            else:
                st.write("No image available for this character.")
    else:
        st.write("No characters created yet.")

# Main function
def main():
    st.title("Character Logbook")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = st.session_state.get("logged_in", False)

    if st.session_state.logged_in:
        st.sidebar.title("Options")
        option = st.sidebar.selectbox("Choose an option", ("Create New Character", "Edit Character", "Load Characters"))

        if option == "Create New Character":
            create_character()
        elif option == "Edit Character":
            edit_character()
        elif option == "Load Characters":
            load_characters()
    else:
        # Login or Register
        login_or_register = st.radio("Login or Register", ("Login", "Register"))
        email = st.text_input("Email")

        if st.button(login_or_register):
            if login_or_register == "Login":
                login_user(email)
            else:
                register_user(email)

if __name__ == "__main__":
    main()
