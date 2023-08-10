import streamlit as st
import sqlite3 as sql3
from streamlit import session_state as ss
import os

from util import *
#new main

def app():
    st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.title("Character Dashboard")

    # Log in page
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Log in page
        names_from_primary_info = get_values_alchemy('primary_info', 'name')
        st.session_state.key = st.selectbox("Select your character", names_from_primary_info)

        if st.button('Log in'):
            # Try to get a character with the entered key as the id
            character = get_character_by_name_alchemy(st.session_state.key)

            # If a character was found, display their information
            if character is not None:
                st.session_state.logged_in = True
                st.session_state.button_clicked = False
                #st.success('Logged in successfully')
                #st.subheader(f"Character Name: {character['name']}")
                #st.text(f"Strength: {character['körperkraft']}")
                #st.text(f"Intelligence: {character['nahkampf']}")  # replace with actual intelligence column
            else:
                st.session_state.button_clicked = True
                st.error('The key you entered is invalid')

        # Create a new character
        if 'show_form' not in ss:
            ss.show_form = False

        if st.button('Create new Character'):
            ss.show_form = not ss.show_form

        if ss.show_form:
            ss.show_form = show_character_submit_form()
    else:
        # Display character information
        character = get_character_by_name_alchemy(st.session_state.key)
        st.write('Character Details')
        st.text(f"Name: {character['name']}", help= f"This value is calculated by KK({character['kk']}) + INT({character['intel']})")
        st.text(f"Rasse: {character['race']}")
        st.text(f"Klasse: {character['class']}")

        if st.button('Go Back'):
            st.session_state.logged_in = False
            st.session_state.button_clicked = False


if __name__ == "__main__":
    app()