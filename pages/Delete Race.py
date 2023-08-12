from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Delete Race")
names_from_primary_info = get_values_alchemy('race', 'name')
st.session_state.delete = st.selectbox("Select race to delete", names_from_primary_info)
if st.button('Delete race'):
    delete_data_alchemy('race', st.session_state.delete)
    st.success(f"Race {st.session_state.delete} was successfully removed.")
    st.toast("Race successfully deleted", icon="✅")
    time.sleep(2)
    st.experimental_rerun()