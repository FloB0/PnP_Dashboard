import streamlit as st
import sqlite3 as sql3
from streamlit import session_state as ss
import os
from util import *


def app():
    st.title("Character Dashboard")

    # Log in page
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if not st.session_state.logged_in:
        # Log in page
        st.session_state.key = st.text_input("Enter your key")

        if st.button('Log in') or st.session_state.button_clicked:
            # Try to get a character with the entered key as the id
            character = get_character_by_id_alchemy(st.session_state.key)

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
            with st.form(key='character_form'):
                # fetch dropdown data
                races = get_values_alchemy('race')
                #classes = get_values_alchemy('class')

                st.write('Character Details')
                name = st.text_input('Name')
                race = st.selectbox('Rasse', races)
                #class_ = st.selectbox('Klasse', classes)

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
                submitted = st.form_submit_button("Submit")

                # If the submit button is clicked, insert the new character into the SQLite database
                if submitted:
                    if name == '':
                        st.warning('Please enter a name before submitting.')
                    else:
                        character = {
                            'name': name,
                            'race': race,
                            #'class': class_,
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
    else:
        # Display character information
        character = get_character_by_id_alchemy(st.session_state.key)
        st.write('Character Details')
        st.text(f"Name: {character['name']}", help= f"This value is calculated by KK({character['kk']}) + INT({character['intel']})")
        st.text(f"Rasse: {character['race']}")
        st.text(f"Klasse: {character['class']}")

        if st.button('Go Back'):
            st.session_state.logged_in = False
            st.session_state.button_clicked = False


if __name__ == "__main__":
    app()