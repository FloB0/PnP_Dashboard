import streamlit as st
import sqlite3 as sql3
from streamlit import session_state as ss
import os

from util import *


# new main

def app():
    st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    print("st.session_state.logged_in: ",st.session_state.logged_in)
    if not st.session_state.logged_in:
        st.title("Character Dashboard")
        names_from_primary_info = get_values_alchemy('primary_info', 'name')
        st.session_state.key = st.selectbox("Select your character", names_from_primary_info)
        if st.button('Log in'):
            print("button pressed")
            character = get_character_by_name_alchemy(st.session_state.key)
            # If a character was found, display their information
            if character is not None:
                st.session_state.logged_in = True
                print("character fetched")
                print("st.session_state.logged_in insinde: ", st.session_state.logged_in)
                st.experimental_rerun()
            else:
                st.error('The key you entered is invalid')
    else:
        if get_character_by_name_alchemy(st.session_state.key) is None:
            st.toast("Character is not valid anymore", icon="🚨")
            st.session_state.logged_in = False
            time.sleep(2)
            st.experimental_rerun()
        #The user is logged in
        character = get_character_by_name_alchemy(st.session_state.key)
        print(character)
        print(type(character))
        st.title(f"{character['name']}")
        st.text(f"Strength: {character['kk']}")
        st.text(f"Intelligence: {character['nahkampf']}")  # replace with actual intelligence column

        if st.button('Go Back'):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    app()
