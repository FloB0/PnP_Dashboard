
import streamlit as st

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="📓",
        layout="wide",
    )

if "active_char" in st.session_state:
    txt = st.text_area('Information to add as note to your character', placeholder= "Enter note here...",height=250)
    st.write('Sentiment: ', "fine")

else:
    st.subheader("No character selected")
    st.write("Please log into a character you want to play.")