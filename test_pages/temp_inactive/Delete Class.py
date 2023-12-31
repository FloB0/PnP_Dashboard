from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Delete Class")
names_from_primary_info = get_values_alchemy('classes', 'name')
st.session_state.delete = st.selectbox("Select class to delete", names_from_primary_info)
if st.button('Delete class'):
    delete_data_alchemy('classes', st.session_state.delete)
    st.success(f"Class {st.session_state.delete} was successfully removed.")
    st.toast("Class successfully deleted", icon="✅")
    time.sleep(2)
    st.experimental_rerun()