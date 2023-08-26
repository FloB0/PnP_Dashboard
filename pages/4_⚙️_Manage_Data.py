from pages import (insert_character, insert_class, insert_item, insert_race, delete_character, delete_item, delete_race, \
                   delete_class, empty_page, insert_stat, delete_stat, update_stat, edit_item)
import streamlit as st

st.set_page_config(
    page_title="DarkDystopia",
    page_icon="⚙️",
    layout="wide",
)

page_names_to_funcs = {
    "-": empty_page,
    "Insert Character": insert_character,
    "Insert Class": insert_class,
    "Insert Item": insert_item,
    "Insert Race": insert_race,
    "Create Stat": insert_stat,
    "Update Stat": update_stat,
    "Delete Character": delete_character,
    "Delete Item": delete_item,
    "Delete Race": delete_race,
    "Delete Class": delete_class,
    "Delete Stat": delete_stat,
    "Edit Item": edit_item,
}

page_name = st.selectbox("Chose what you want to do:", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
