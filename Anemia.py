import streamlit as st

def get_normal_ranges(age, gender):
    """
    Function to get normal ranges for CBC parameters based on age and gender.
    """
    normal_ranges = {
        "Hemoglobin": (13.5, 17.5) if gender == "Male" else (12.0, 15.5),
        "Mean Corpuscular Volume (MCV)": (80, 100),
        "Mean Corpuscular Hemoglobin (MCH)": (27, 31),
        "Leukocytes": (4.0, 11.0),
        "Thrombocytes": (150, 400),
        "Erythrocytes": (4.2, 5.4),
        "Reticulocytes": (0.5, 1.5),
        "MCHC": (32, 36)
    }

    # Adjust normal ranges based on age
    if age > 60:
        normal_ranges["Hemoglobin"] = (13.0, 16.5) if gender == "Male" else (11.5, 15.0)
        normal_ranges["Erythrocytes"] = (4.0, 5.2)

    return normal_ranges

def classify_anemia(parameters):
    """
    Function to classify anemia based on CBC parameters.
    Add your classification logic here.
    """
    hemoglobin = parameters["Hemoglobin"]
    mcv = parameters["Mean Corpuscular Volume (MCV)"]
    # Add your classification logic here based on the provided parameters
    return "No specific type detected"

def main():
    st.title("Anemia Classification App")
    st.subheader("Enter Complete Blood Count Parameters")

    # Input fields for age and gender
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])

    # Get normal ranges based on age and gender
    normal_ranges = get_normal_ranges(age, gender)

    # Input fields for CBC parameters
    parameters = {}
    for parameter, (min_value, max_value) in normal_ranges.items():
        parameters[parameter] = st.number_input(parameter, min_value=0.0, max_value=1000.0, step=0.1)

    # Check if values are within normal range and mark fields red if not
    for parameter, (min_value, max_value) in normal_ranges.items():
        if parameters[parameter] < min_value or parameters[parameter] > max_value:
            st.markdown(f"<span style='color:red'>{parameter} is out of normal range!</span>", unsafe_allow_html=True)

    if st.button("Classify"):
        anemia_type = classify_anemia(parameters)
        st.write(f"Based on the provided parameters, you may have: {anemia_type}")

if __name__ == "__main__":
    main()
