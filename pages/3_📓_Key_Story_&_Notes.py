import streamlit as st
from util import insert_data_alchemy, on_note_submit_click
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="📓",
        layout="wide",
    )
if "note_submitted" not in st.session_state:
    st.session_state.note_submitted = False

if "active_char" in st.session_state:
    with st.form(key='note_form', clear_on_submit=True):
        txt = st.text_area('Information to add as note to your character', placeholder="Enter note here...", height=250)
        # Create the submit button
        st.form_submit_button("Submit", on_click=on_note_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('note_submitted', True):
            data_out = {
                'characterID': st.session_state['active_char']['id'],
                'notes': txt
            }
            insert_data_alchemy('character_notes', data_out)
            st.success('Note added.')
            st.session_state.note_submitted = False
            st.session_state.show_form = False
            st.toast("Note added.. Reloading..", icon="✅")
            time.sleep(2)
            st.experimental_rerun()
else:
    st.subheader("No character selected")
    st.write("Please log into a character you want to play.")