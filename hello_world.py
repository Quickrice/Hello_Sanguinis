# Streamlit hello world app
import streamlit as st

def main():
    st.title('Hello World!')
    st.write('This is a simple hello world app in Streamlit.')
    st.write('To run this app, use the following command:')
    st.code('streamlit run hello_world.py')

if __name__ == '__main__':
    main()
