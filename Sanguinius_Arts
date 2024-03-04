import streamlit as st
import plotly.express as px

def main():
    st.title('Sanguis')
    st.header('Mysterium Obscurum: Sanguis Est Via Ad Potentiam')
    st.subheader('Ritus invocote:')
    st.code('streamlit run Ritus Sanguinis.py')
    st.markdown("*Occult* is **really** ***hot***.")
    st.markdown('''
    :red[Sanguis est via ad potentiam, arcanum magicae].''')
    

    # Function to get user input for percentage of each component
    def get_user_input(label, default_value=50):
        return st.slider(f"percentagium de {label} (%)", min_value=0, max_value=100, value=default_value)

    # Pre-set default percentages
    default_values = {'Erythrocytae': 40, 'Leukocytae': 1, 'Thrombocytae': 1, 'Plasma': 58}

    # Sidebar inputs
    st.sidebar.title('recede')
    with st.sidebar:
        st.subheader('Adhuc hic? Abi!')
       

    # Get user input for each component
    erythrocytae_percent = get_user_input('Erythrocytae', default_values['Erythrocytae'])
    leukocytae_percent = get_user_input('Leukocytae', default_values['Leukocytae'])
    thrombocytae_percent = get_user_input('Thrombocytae', default_values['Thrombocytae'])
    plasma_percent = get_user_input('Plasma', default_values['Plasma'])

    # Calculate total percentage
    total_percent = erythrocytae_percent + leukocytae_percent + thrombocytae_percent + plasma_percent

    # Check if total percentage is 100, if not, adjust values
    if total_percent != 100:
        st.warning("Total percentage does not equal 100. Adjusting values to correct.")
        # Adjust values to make total 100
        erythrocytae_percent = erythrocytae_percent / total_percent * 100
        leukocytae_percent = leukocytae_percent / total_percent * 100
        thrombocytae_percent = thrombocytae_percent / total_percent * 100
        plasma_percent = plasma_percent / total_percent * 100

    # Sample data
    labels = ['Erythrocytae', 'Leukocytae', 'Thrombocytae', 'Plasma']
    values = [erythrocytae_percent, leukocytae_percent, thrombocytae_percent, plasma_percent]

    # Create a pie chart
    fig = px.pie(values=values, names=labels, color_discrete_sequence=px.colors.qualitative.Set1)

    # Update layout to add text inside the pie pieces
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Update colors to have red nuances
    fig.update_traces(marker=dict(colors=['#FF5733', '#FF8C33', '#FFBB33', '#FFD433']))

    # Set layout title
    fig.update_layout(title='elementa hematocriti')

    # Render the pie chart
    st.plotly_chart(fig)

    option = st.selectbox(
    'Intellegisne sanguinem tuum?',
    ('ita', 'non', 'nescio'))

    st.write('tu elegisti:', option)

if __name__ == '__main__':
    main()
