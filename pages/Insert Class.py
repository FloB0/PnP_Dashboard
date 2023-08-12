from util import *
import time

st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded"
    )
st.title("Insert Class")
with st.form(key='class_form', clear_on_submit=True):
    name = st.text_input('Name')
    # Create the submit button
    st.form_submit_button("Submit", on_click=on_submit_click)

    # If the submit button is clicked, insert the new character into the SQLite database
    if st.session_state.get('submitted', False):
        if name == '':
            st.warning('Please enter a name before submitting.')
        elif name in get_values_alchemy('classes', 'name'):
            st.warning('Name already taken. Please try something else')
        else:
            classes = {
                'name': name,
            }
            insert_data_alchemy('classes', classes)
            st.success('Class created successfully!')
            st.session_state.submitted = False
            st.session_state.show_form = False
            st.toast("Class successfully addded", icon="✅")
            time.sleep(2)
            st.experimental_rerun()