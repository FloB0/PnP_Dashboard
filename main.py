import streamlit as st

st.set_page_config(
    page_title="DarkDystopia",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

from util import *


def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Character Dashboard")
        names_from_primary_info = get_values_alchemy('primary_info', 'name')
        st.session_state.key = st.selectbox("Select your character", names_from_primary_info)
        if st.button('Log in'):
            character = get_character_by_name_alchemy(st.session_state.key)
            # If a character was found, display their information
            if character is not None:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error('The key you entered is invalid')
    else:
        character = get_character_by_name_alchemy(st.session_state.key)
        if character is None:
            st.toast("Character is not valid anymore", icon="🚨")
            st.session_state.logged_in = False
            time.sleep(2)
            st.experimental_rerun()
        # The user is logged in
        st.title(f"{character['name']}")
        st.divider()
        tab1, tab2, tab3 = st.tabs(["Character Stats", "Items", "Key Notes"])
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                c4, c5, c6, c7 = st.columns([5,2,1,1])
                st.write('Physis')
                with c4:

                    st.text(f"Körperkraft:")
                    st.text(f"Ausdauer:                 {character['a']}")
                    st.text(f"Präzision                 {character['a']}")
                    st.text(f"Physische Belbarkeitast   {character['pb']}")
                    st.text(f"Verhindern                {character['v']}")
                with c5:

                    st.markdown('<p class="big-font">0</p>', unsafe_allow_html=True)
                    # st.write(character['kk'])
                with c6:
                    st.button(label="+1", key=0)
                    st.button(label="+1", key=1)
                    st.button(label="+1", key=2)
                    st.button(label="+1", key=3)
                    st.button(label="+1", key=4)

                with c7:
                    st.button(label="-1", key=5)
                    st.button(label="-1", key=6)
                    st.button(label="-1", key=7)
                    st.button(label="-1", key=8)
                    st.button(label="-1", key=9)
            with c2:
                st.write('Psyche')
                st.text(f"Intelligenz: {character['intel']}")
                st.text(f"Willenskraft: {character['wk']}")
                st.text(f"Wahrnehmung {character['wa']}")
                st.text(f"Mentale Belastbarkeit {character['mb']}")
                st.text(f"Inspiration {character['ins']}")
            with c3:
                st.write('Talente')
                st.text(f"Initiative: {character['ini']}")
                st.text(f"Technisches Verständnis: {character['tv']}")
                st.text(f"Glück {character['g']}")
                st.text(f"Wissen {character['wi']}")
                st.text(f"Charisma {character['c']}")

        with tab2:
            create_item_elements_for_character_id(character["id"])
            st.divider()
            item_names = get_values_alchemy(table_name='items', column_name='name')
            item_to_add = st.selectbox('Add Item', item_names)
            if st.button("Add Item"):
                add_item_to_character(character['id'], item_to_add)
                st.toast("Item added to your character", icon="✅")
                time.sleep(1)
                st.experimental_rerun()

        with tab3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

        if st.button('Log Out'):
            st.session_state.logged_in = False
            st.experimental_rerun()


if __name__ == "__main__":
    app()
