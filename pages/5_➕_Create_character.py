from util import get_values_alchemy, on_submit_click, insert_character_alchemy
import streamlit as st
import time

def app():
    """

    :return:
    """
    st.title("Create Character")

    with st.form(key='character_form', clear_on_submit=True):
        # fetch dropdown data
        races = get_values_alchemy('race', 'name')
        classes = get_values_alchemy('classes', 'name')

        st.write('Character Details')
        name = st.text_input('Name')
        race = st.selectbox('Rasse', races)
        class_ = st.selectbox('Klasse', classes)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.write('Physis')
            kk = st.number_input('Körperkraft', value=0, step=1)
            a = st.number_input('Ausdauer', value=0, step=1)
            p = st.number_input('Präzision', value=0, step=1)
            pb = st.number_input('Physische Belastbarkeit', value=0, step=1)
            v = st.number_input('Verhindern', value=0, step=1)
        with c2:
            st.write('Psyche')
            intel = st.number_input('Intelligenz', value=0, step=1)
            wk = st.number_input('Willenskraft', value=0, step=1)
            wa = st.number_input('Wahrnehmung', value=0, step=1)
            mb = st.number_input('Mentale Belastbarkeit', value=0, step=1)
            ins = st.number_input('Inspiration', value=0, step=1)
        with c3:
            st.write('Talente')
            ini = st.number_input('Initiative', value=0, step=1)
            tv = st.number_input('Technisches Verständnis', value=0, step=1)
            g = st.number_input('Glück', value=0, step=1)
            wi = st.number_input('Wissen', value=0, step=1)
            c = st.number_input('Charisma', value=0, step=1)

        # Create the submit button
        st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            if name == '':
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('primary_info', 'name'):
                st.warning('Name already taken. Please try something else')
            else:
                character = {
                    'name': name,
                    'race': race,
                    'class': class_,
                    'kk': kk,
                    'a': a,
                    'p': p,
                    'pb': pb,
                    'v': v,
                    'intel': intel,
                    'wk': wk,
                    'wa': wa,
                    'mb': mb,
                    'ins': ins,
                    'ini': ini,
                    'tv': tv,
                    'g': g,
                    'wi': wi,
                    'c': c,
                    'created_by': st.session_state.USERNAME
                    }
                insert_character_alchemy(character)
                st.success('Character created successfully!')
                st.session_state.submitted = False
                st.session_state.show_form = False
                st.toast("Character successfully addded", icon="✅")
                time.sleep(2)
                st.experimental_rerun()
    return

if __name__ == "__main__":
    if st.session_state.LOGGED_IN:
        app()
    else:
        st.write("Not authenticated. Please log in.")