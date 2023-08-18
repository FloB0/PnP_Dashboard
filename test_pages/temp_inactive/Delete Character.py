from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Delete Character")
names_from_primary_info = get_values_alchemy('primary_info', 'name')
st.session_state.delete = st.selectbox("Select your character", names_from_primary_info)
if st.button('Delete Character'):
    delete_character_alchemy(st.session_state.delete)
    st.success(f"Character {st.session_state.delete} was successfully removed.")
    st.toast("Character successfully deleted", icon="✅")
    time.sleep(2)
    st.experimental_rerun()