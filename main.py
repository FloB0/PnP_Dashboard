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
        initial_sidebar_state="expanded"
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

        if 'show_form' not in st.session_state:
            st.session_state.show_form = False

        if st.button('Create new Character'):
            st.session_state.show_form = not st.session_state.show_form

        if st.session_state.show_form:
            if 'submitted' not in st.session_state:
                st.session_state.submitted = False

            with st.form(key='character_form'):
                # fetch dropdown data
                races = get_values_alchemy('race', 'name')
                # classes = get_values_alchemy('class')

                st.write('Character Details')
                name = st.text_input('Name')
                race = st.selectbox('Rasse', races)
                # class_ = st.selectbox('Klasse', classes)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write('Pysis')
                    kk = st.number_input('Körperkraft', value=0, step=1)
                    a = st.number_input('Ausdauer', value=0, step=1)
                    p = st.number_input('Präzision', value=0, step=1)
                    pb = st.number_input('Physische Belastbarkeit', value=0, step=1)
                    v = st.number_input('Verhindern', value=0, step=1)
                with c2:
                    st.write('Psyche')
                    intel = st.number_input('Intelligenz', value=0, step=1)
                    wk = st.number_input('Willenskraft', value=0, step=1)
                    wa = st.number_input('Wahrnehmung', value=0, step=1)
                    mb = st.number_input('Mentale Belastbarkeit', value=0, step=1)
                    ins = st.number_input('Inspiration', value=0, step=1)
                with c3:
                    st.write('Talente')
                    ini = st.number_input('Initiative', value=0, step=1)
                    tv = st.number_input('Technisches Verständnis', value=0, step=1)
                    g = st.number_input('Glück', value=0, step=1)
                    wi = st.number_input('Wissen', value=0, step=1)
                    c = st.number_input('Charisma', value=0, step=1)

                # Create the submit button
                st.form_submit_button("Submit", on_click=on_submit_click)

                # If the submit button is clicked, insert the new character into the SQLite database
                if st.session_state.get('submitted', False):
                    if name == '':
                        st.warning('Please enter a name before submitting.')
                    elif name in get_values_alchemy('primary_info', 'name'):
                        st.warning('Name already taken. Please try something else')
                    else:
                        character = {
                            'name': name,
                            'race': race,
                            # 'class': class_,
                            'kk': kk,
                            'a': a,
                            'p': p,
                            'pb': pb,
                            'v': v,
                            'intel': intel,
                            'wk': wk,
                            'wa': wa,
                            'mb': mb,
                            'ins': ins,
                            'ini': ini,
                            'tv': tv,
                            'g': g,
                            'wi': wi,
                            'c': c
                        }
                        insert_character_alchemy(character)
                        st.success('Character created successfully!')
                        st.session_state.submitted = False
                        st.session_state.show_form = False
                        st.experimental_rerun()

    else:
        #The user is logged in
        character = get_character_by_name_alchemy(st.session_state.key)
        st.title(f"{character['name']}")
        st.text(f"Strength: {character['kk']}")
        st.text(f"Intelligence: {character['nahkampf']}")  # replace with actual intelligence column

        if st.button('Go Back'):
            st.session_state.logged_in = False
            st.experimental_rerun()


def app_idea():
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
                # st.success('Logged in successfully')
                # st.subheader(f"Character Name: {character['name']}")
                # st.text(f"Strength: {character['körperkraft']}")
                # st.text(f"Intelligence: {character['nahkampf']}")  # replace with actual intelligence column
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
        st.text(f"Name: {character['name']}",
                help=f"This value is calculated by KK({character['kk']}) + INT({character['intel']})")
        st.text(f"Rasse: {character['race']}")
        st.text(f"Klasse: {character['class']}")

        if st.button('Go Back'):
            st.session_state.logged_in = False


if __name__ == "__main__":
    app()
