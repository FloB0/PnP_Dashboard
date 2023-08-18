from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Insert Item")
with st.form(key='item_form', clear_on_submit=True):
    name = st.text_input('Name')
    description = st.text_input('Description')
    image_url = st.text_input('Image-URL', value="https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/")
    # Create the submit button
    st.form_submit_button("Submit", on_click=on_submit_click)

    # If the submit button is clicked, insert the new character into the SQLite database
    if st.session_state.get('submitted', False):
        if name == '':
            st.warning('Please enter a name before submitting.')
        elif name in get_values_alchemy('classes', 'name'):
            st.warning('Name already taken. Please try something else')
        else:
            items = {
                'name': name,
                'description': description,
                'image_url' : image_url
            }
            insert_data_alchemy('items', name)
            st.success('Item created successfully!')
            st.session_state.submitted = False
            st.session_state.show_form = False
            st.toast("Item successfully addded", icon="✅")
            time.sleep(2)
            st.experimental_rerun()