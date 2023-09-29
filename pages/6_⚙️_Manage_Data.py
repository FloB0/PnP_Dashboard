from pages import (
    insert_character, insert_class, insert_item, insert_race, delete_character, delete_item, delete_race, \
    delete_class, empty_page, insert_stat, delete_stat, update_stat, edit_item, insert_trait, update_trait, edit_trait,
    delete_trait, add_trait_to_character, link_stat_trait_to_race, link_stat_trait_to_class, manage_user_rights,
    create_timeline, create_event, connect_event_timeline
    )
import streamlit as st
import os
from util import on_submit_click
from time import sleep

ADMIN_AUTH_TOKEN = os.environ.get("ADMIN_AUTH_TOKEN")

st.set_page_config(
    page_title="DarkDystopia",
    page_icon="⚙️",
    layout="wide",
    )


def app():
    page_names_to_funcs = {
        "-": empty_page,
        # "Insert Character": insert_character, # this page moved to a own page accessible by users
        "Insert Class": insert_class,
        "Insert Item": insert_item,
        "Insert Race": insert_race,
        "Insert Trait": insert_trait,
        "Create Stat": insert_stat,
        "Update Stat": update_stat,
        "Update Trait": update_trait,
        "Edit Item": edit_item,
        "Edit Trait": edit_trait,
        "Delete Character": delete_character,
        "Delete Item": delete_item,
        "Delete Race": delete_race,
        "Delete Class": delete_class,
        "Delete Stat": delete_stat,
        "Delete Trait": delete_trait,
        "Add/Delete Trait to/from character": add_trait_to_character,
        "Add/Delete Trait/stat from race": link_stat_trait_to_race,
        "Add/Delete Trait/stat from class": link_stat_trait_to_class,
        "Manage User Rights": manage_user_rights,
        "Create a Timeline": create_timeline,
        "Create an Event": create_event,
        "Connect Events to a Timeline": connect_event_timeline
        }

    page_name = st.selectbox("Chose what you want to do:", page_names_to_funcs.keys())
    page_names_to_funcs[page_name]()


if __name__ == "__main__":
    if not (st.session_state.AUTHENTICATED or st.session_state.ADMIN):
        with st.form(key='auth_token', clear_on_submit=True):
            inToken = st.text_input(label= "Authentication Token")
            st.form_submit_button("Submit", on_click=on_submit_click)

            if st.session_state.get('submitted', False):
                if inToken == ADMIN_AUTH_TOKEN:
                    st.toast("Authentication successful", icon="✅")
                    st.session_state.AUTHENTICATED = True
                    sleep(2)
                else:
                    st.toast("Authentication not successful", icon="🚨")
                    sleep(2)
    if st.session_state.AUTHENTICATED and st.session_state.LOGGED_IN:
        app()
    if not st.session_state.LOGGED_IN:
        st.write("Please login to access this content.")
    if not st.session_state.ADMIN and not (st.session_state.AUTHENTICATED and st.session_state.LOGGED_IN):
        st.write("You are not an admin. Please use admin account or contact the support team.")
    if st.session_state.LOGGED_IN and st.session_state.ADMIN:
        app()
