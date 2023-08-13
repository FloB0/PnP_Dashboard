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

    print("st.session_state.logged_in: ",st.session_state.logged_in)
    if not st.session_state.logged_in:
        st.title("Character Dashboard")
        names_from_primary_info = get_values_alchemy('primary_info', 'name')
        st.session_state.key = st.selectbox("Select your character", names_from_primary_info)
        if st.button('Log in'):
            print("button pressed")
            character = get_character_by_name_alchemy(st.session_state.key)
            # If a character was found, display their information
            if character is not None:
                st.session_state.logged_in = True
                print("character fetched")
                print("st.session_state.logged_in insinde: ", st.session_state.logged_in)
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
                # st.write('Psyche')
                # intel = st.number_input('Intelligenz', value=0, step=1)
                # wk = st.number_input('Willenskraft', value=0, step=1)
                # wa = st.number_input('Wahrnehmung', value=0, step=1)
                # mb = st.number_input('Mentale Belastbarkeit', value=0, step=1)
                # ins = st.number_input('Inspiration', value=0, step=1)
            with c3:
                st.text('Talente')
                st.text(f"Initiative: {character['ini']}")
                st.text(f"Technisches Verständnis: {character['tv']}")
                st.text(f"Glück {character['g']}")
                st.text(f"Wissen {character['wi']}")
                st.text(f"Charisma {character['c']}")
                # st.write('Talente')
                # ini = st.number_input('Initiative', value=0, step=1)
                # tv = st.number_input('Technisches Verständnis', value=0, step=1)
                # g = st.number_input('Glück', value=0, step=1)
                # wi = st.number_input('Wissen', value=0, step=1)
                # c = st.number_input('Charisma', value=0, step=1)

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


        with tab3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

        if st.button('Go Back'):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    app()
