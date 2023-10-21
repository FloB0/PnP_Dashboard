from util import create_item_elements_for_character_id, get_values_alchemy, add_item_to_character
import time
import streamlit as st
from types import SimpleNamespace
from classes_dashborad import *

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🏹",
        layout="wide",
    )


def app():
    if "active_char" in st.session_state:
        create_item_elements_for_character_id(st.session_state.active_char["id"])
        st.divider()
        item_names_ = get_values_alchemy(table_name='items', column_names=['name'])
        item_names = [d["name"] for d in item_names_]

        item_to_add = st.selectbox('Add Item', item_names)
        if st.button("Add Item"):
            add_item_to_character(st.session_state.active_char['id'], item_to_add)
            st.toast("Item added to your character", icon="✅")
            time.sleep(1)
            st.experimental_rerun()
    else:
        st.subheader("No character selected")
        st.write("Please log into a character you want to play.")


if __name__ == "__main__":
    if st.session_state.LOGGED_IN:
        app()
    else:
        st.write("Not authenticated. Please log in.")