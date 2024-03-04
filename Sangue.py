import streamlit as st
import plotly.express as px

def main():
    st.title('Sanguis')
    st.header('Mysterium Obscurum: Sanguis Est Via Ad Potentiam')
    st.subheader('Ritus invocote:')
    st.markdown("*Occult* is **really** ***hot***.")
    st.markdown('''
    :red[Sanguis est via ad potentiam, arcanum magicae].''')

    # Function to get user input for percentage of each component
    def get_user_input(label):
        return st.slider(f"Percentagium de {label} (%)", min_value=0, max_value=100, value=50)

    # Get user input for each component
    erythrocytae_percent = get_user_input('Erythrocytae')
    leukocytae_percent = get_user_input('Leukocytae')
    thrombocytae_percent = get_user_input('Thrombocytae')
    plasma_percent = get_user_input('Plasma')

    # Sample data
    labels = ['Erythrocytae', 'Leukocytae', 'Thrombocytae', 'Plasma']
    values = [erythrocytae_percent, leukocytae_percent, thrombocytae_percent, plasma_percent]

    # Render the pie chart
    fig = px.pie(values=values, names=labels, color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig)

    option = st.selectbox(
        'Intellegisne sanguinem tuum?',
        ('Ita', 'Non', 'Nescio')
    )
    st.write('Tu elegisti:', option)

if __name__ == '__main__':
    main()
