import streamlit

from util import *
from streamlit_elements import elements, mui, html

def app():
    st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
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
        #The user is logged in
        st.title(f"{character['name']}")
        tab1, tab2, tab3 = st.tabs(["Character Stats", "Items", "Key Notes"])
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write('Physis')
                st.text(f"Körperkraft: {character['kk']}")
                st.text(f"Ausdauer: {character['a']}")
                st.text(f"Präzision {character['a']}")
                st.text(f"Physische Belbarkeitast {character['pb']}")
                st.text(f"Verhindern {character['v']}")
            with c2:
                st.text('Psyche')
                st.text(f"Intelligenz: {character['intel']}")
                st.text(f"Willenskraft: {character['wk']}")
                st.text(f"Wahrnehmung {character['wa']}")
                st.text(f"Mentale Belastbarkeit {character['mb']}")
                st.text(f"Inspiration {character['ins']}")
            with c3:
                st.text('Talente')
                st.text(f"Initiative: {character['ini']}")
                st.text(f"Technisches Verständnis: {character['tv']}")
                st.text(f"Glück {character['g']}")
                st.text(f"Wissen {character['wi']}")
                st.text(f"Charisma {character['c']}")

        with tab2:
            with elements("dashboard"):
                # You can create a draggable and resizable dashboard using
                # any element available in Streamlit Elements.

                from streamlit_elements import dashboard

                # First, build a default layout for every element you want to include in your dashboard

                layout = [
                    # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
                    dashboard.Item("first_item", 0, 0, 2, 2),
                    dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=True),
                    dashboard.Item("third_item", 0, 2, 1, 1, isResizable=True),
                ]

                # Next, create a dashboard layout using the 'with' syntax. It takes the layout
                # as first parameter, plus additional properties you can find in the GitHub links below.

                with dashboard.Grid(layout):
                    mui.Paper("First item", key="first_item")
                    mui.Paper("Second item (cannot drag)", key="second_item")
                    mui.Paper("Third item (cannot resize)", key="third_item")
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
