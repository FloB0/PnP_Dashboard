from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Delete Item")
names_from_primary_info = get_values_alchemy('items', 'name')
st.session_state.delete = st.selectbox("Select item to delete", names_from_primary_info)
if st.button('Delete item'):
    delete_data_alchemy('items', st.session_state.delete)
    st.success(f"Item {st.session_state.delete} was successfully removed.")
    st.toast("Item successfully deleted", icon="✅")
    time.sleep(2)
    st.experimental_rerun()