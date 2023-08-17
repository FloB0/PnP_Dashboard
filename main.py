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
    font-size:24.5px !important;
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
        if "char_fetched" not in st.session_state:
            st.session_state.char_fetched = False

        if not st.session_state.char_fetched:
            character = get_character_by_name_alchemy(st.session_state.key)
            st.session_state.active_char = character
            st.session_state.char_fetched = True

        if 'active_char' not in st.session_state:
            st.toast("Character is not valid anymore", icon="🚨")
            st.session_state.logged_in = False
            st.session_state.char_fetched = False
            time.sleep(2)
            st.experimental_rerun()
        # The user is logged in
        st.title(f"{st.session_state.active_char['name']}")
        st.divider()
        tab1, tab2, tab3 = st.tabs(["Character Stats", "Items", "Key Notes"])
        with tab1:
            c100, c110, c120 = st.columns(3)
            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = st.columns([5, 2, 1, 1, 5, 2, 1, 1, 5, 2, 1, 1])

            with st.container():
                c100.markdown(f'<p class="big-font">Physis</p>', unsafe_allow_html=True)
                c110.markdown(f'<p class="big-font">Psyche</p>', unsafe_allow_html=True)
                c120.markdown(f'<p class="big-font">Talente</p>', unsafe_allow_html=True)
            with st.container():
                c1.markdown(f'<p class="big-font">Körperkraft</p>', unsafe_allow_html=True)
                c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['kk']),
                            unsafe_allow_html=True)
                c3.button(label="+1", key=100, on_click=increment_stat, args=('kk',))
                c4.button(label="-1", key=101, on_click=decrement_stat, args=('kk',))
                c5.markdown(f'<p class="big-font">Intelligenz</p>', unsafe_allow_html=True)
                c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['intel']),
                            unsafe_allow_html=True)
                c7.button(label="+1", key=102, on_click=increment_stat, args=('intel',))
                c8.button(label="-1", key=103, on_click=decrement_stat, args=('intel',))
                c9.markdown(f'<p class="big-font">Initiative</p>', unsafe_allow_html=True)
                c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ini']),
                             unsafe_allow_html=True)
                c11.button(label="+1", key=104, on_click=increment_stat, args=('ini',))
                c12.button(label="-1", key=105, on_click=decrement_stat, args=('ini',))
            with st.container():
                c1.markdown(f'<p class="big-font">Ausdauer</p>', unsafe_allow_html=True)
                c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['a']),
                            unsafe_allow_html=True)
                c3.button(label="+1", key=106, on_click=increment_stat, args=('a',))
                c4.button(label="-1", key=107, on_click=decrement_stat, args=('a',))
                c5.markdown(f'<p class="big-font">Willenskraft</p>', unsafe_allow_html=True)
                c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wk']),
                            unsafe_allow_html=True)
                c7.button(label="+1", key=108, on_click=increment_stat, args=('wk',))
                c8.button(label="-1", key=109, on_click=decrement_stat, args=('wk',))
                c9.markdown(f'<p class="big-font">Technisches Verständnis</p>', unsafe_allow_html=True)
                c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['tv']),
                             unsafe_allow_html=True)
                c11.button(label="+1", key=110, on_click=increment_stat, args=('tv',))
                c12.button(label="-1", key=111, on_click=decrement_stat, args=('tv',))
            with st.container():
                c1.markdown(f'<p class="big-font">Präzision</p>', unsafe_allow_html=True)
                c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p']),
                            unsafe_allow_html=True)
                c3.button(label="+1", key=112, on_click=increment_stat, args=('p',))
                c4.button(label="-1", key=113, on_click=decrement_stat, args=('p',))
                c5.markdown(f'<p class="big-font">Wahrnehmung</p>', unsafe_allow_html=True)
                c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wa']),
                            unsafe_allow_html=True)
                c7.button(label="+1", key=114, on_click=increment_stat, args=('wa',))
                c8.button(label="-1", key=115, on_click=decrement_stat, args=('wa',))
                c9.markdown(f'<p class="big-font">Glück</p>', unsafe_allow_html=True)
                c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['g']),
                             unsafe_allow_html=True)
                c11.button(label="+1", key=116, on_click=increment_stat, args=('g',))
                c12.button(label="-1", key=117, on_click=decrement_stat, args=('g',))
            with st.container():
                c1.markdown(f'<p class="big-font">Physische Belastbarkeit</p>', unsafe_allow_html=True)
                c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['pb']),
                            unsafe_allow_html=True)
                c3.button(label="+1", key=118, on_click=increment_stat, args=('pb',))
                c4.button(label="-1", key=119, on_click=decrement_stat, args=('pb',))
                c5.markdown(f'<p class="big-font">Mentale Belastbarkeit</p>', unsafe_allow_html=True)
                c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['mb']),
                            unsafe_allow_html=True)
                c7.button(label="+1", key=120, on_click=increment_stat, args=('mb',))
                c8.button(label="-1", key=121, on_click=decrement_stat, args=('mb',))
                c9.markdown(f'<p class="big-font">Wissen</p>', unsafe_allow_html=True)
                c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wi']),
                             unsafe_allow_html=True)
                c11.button(label="+1", key=122, on_click=increment_stat, args=('wi',))
                c12.button(label="-1", key=123, on_click=decrement_stat, args=('wi',))
            with st.container():
                c1.markdown(f'<p class="big-font">Verhindern</p>', unsafe_allow_html=True)
                c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['v']),
                            unsafe_allow_html=True)
                c3.button(label="+1", key=124, on_click=increment_stat, args=('v',))
                c4.button(label="-1", key=125, on_click=decrement_stat, args=('v',))
                c5.markdown(f'<p class="big-font">Inspiration</p>', unsafe_allow_html=True)
                c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ins']),
                            unsafe_allow_html=True)
                c7.button(label="+1", key=126, on_click=increment_stat, args=('ins',))
                c8.button(label="-1", key=127, on_click=decrement_stat, args=('ins',))
                c9.markdown(f'<p class="big-font">Charisma</p>', unsafe_allow_html=True)
                c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['c']),
                             unsafe_allow_html=True)
                c11.button(label="+1", key=128, on_click=increment_stat, args=('c',))
                c12.button(label="-1", key=129, on_click=decrement_stat, args=('c',))

            st.divider()
            st.subheader("Secondary Abilities")
            c101, c111, c121, c131 = st.columns(4)
            c21, c22, c23, c24, c25, c26, c27, c28, c29, c210, c211, c212, c213, c214, c215, c216= st.columns([4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1])
            with st.container():
                c101.markdown(f'<p class="big-font">Gefecht</p>', unsafe_allow_html=True)
                c111.markdown(f'<p class="big-font">Gewandtheit</p>', unsafe_allow_html=True)
                c121.markdown(f'<p class="big-font">Gesellschaft</p>', unsafe_allow_html=True)
                c131.markdown(f'<p class="big-font">Wissen</p>', unsafe_allow_html=True)
            with st.container():
                c21.markdown(f'<p class="big-font">Nahkampf</p>', unsafe_allow_html=True)
                c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['nahkampf']),
                            unsafe_allow_html=True)
                c23.button(label="+1", key=130, on_click=increment_stat, args=('nahkampf',))
                c24.button(label="-1", key=131, on_click=decrement_stat, args=('nahkampf',))
                c25.markdown(f'<p class="big-font">Ausweichen</p>', unsafe_allow_html=True)
                c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ausweichen']),
                            unsafe_allow_html=True)
                c27.button(label="+1", key=132, on_click=increment_stat, args=('ausweichen',))
                c28.button(label="-1", key=133, on_click=decrement_stat, args=('ausweichen',))
                c29.markdown(f'<p class="big-font">Lügen</p>', unsafe_allow_html=True)
                c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['luegen']),
                             unsafe_allow_html=True)
                c211.button(label="+1", key=134, on_click=increment_stat, args=('luegen',))
                c212.button(label="-1", key=135, on_click=decrement_stat, args=('luegen',))
                c213.markdown(f'<p class="big-font">Mechanik</p>', unsafe_allow_html=True)
                c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['mechanik']),
                              unsafe_allow_html=True)
                c215.button(label="+1", key=136, on_click=increment_stat, args=('mechanik',))
                c216.button(label="-1", key=137, on_click=decrement_stat, args=('mechanik',))
            with st.container():
                c21.markdown(f'<p class="big-font">Fermkampf</p>', unsafe_allow_html=True)
                c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['fernkampf']),
                            unsafe_allow_html=True)
                c23.button(label="+1", key=138, on_click=increment_stat, args=('fernkampf',))
                c24.button(label="-1", key=139, on_click=decrement_stat, args=('fernkampf',))
                c25.markdown(f'<p class="big-font">Tarnung</p>', unsafe_allow_html=True)
                c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['tarnung']),
                            unsafe_allow_html=True)
                c27.button(label="+1", key=140, on_click=increment_stat, args=('tarnung',))
                c28.button(label="-1", key=141, on_click=decrement_stat, args=('tarnung',))
                c29.markdown(f'<p class="big-font">Etikette</p>', unsafe_allow_html=True)
                c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['etikette']),
                             unsafe_allow_html=True)
                c211.button(label="+1", key=142, on_click=increment_stat, args=('etikette',))
                c212.button(label="-1", key=143, on_click=decrement_stat, args=('etikette',))
                c213.markdown(f'<p class="big-font">Ätherkunde</p>', unsafe_allow_html=True)
                c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['aetherkunde']),
                              unsafe_allow_html=True)
                c215.button(label="+1", key=144, on_click=increment_stat, args=('aetherkunde',))
                c216.button(label="-1", key=145, on_click=decrement_stat, args=('aetherkunde',))
            with st.container():
                c21.markdown(f'<p class="big-font">Parieren</p>', unsafe_allow_html=True)
                c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['parieren']),
                            unsafe_allow_html=True)
                c23.button(label="+1", key=146, on_click=increment_stat, args=('parieren',))
                c24.button(label="-1", key=147, on_click=decrement_stat, args=('parieren',))
                c25.markdown(f'<p class="big-font">Fingerfertigkeit</p>', unsafe_allow_html=True)
                c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['fingerfertigkeit']),
                            unsafe_allow_html=True)
                c27.button(label="+1", key=148, on_click=increment_stat, args=('fingerfertigkeit',))
                c28.button(label="-1", key=149, on_click=decrement_stat, args=('fingerfertigkeit',))
                c29.markdown(f'<p class="big-font">Handeln</p>', unsafe_allow_html=True)
                c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['handeln']),
                             unsafe_allow_html=True)
                c211.button(label="+1", key=150, on_click=increment_stat, args=('handeln',))
                c212.button(label="-1", key=151, on_click=decrement_stat, args=('handeln',))
                c213.markdown(f'<p class="big-font">Xenos</p>', unsafe_allow_html=True)
                c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['xenos']),
                              unsafe_allow_html=True)
                c215.button(label="+1", key=152, on_click=increment_stat, args=('xenos',))
                c216.button(label="-1", key=153, on_click=decrement_stat, args=('xenos',))
            with st.container():
                c21.markdown(f'<p class="big-font">Entweichen</p>', unsafe_allow_html=True)
                c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['entweichen']),
                            unsafe_allow_html=True)
                c23.button(label="+1", key=154, on_click=increment_stat, args=('entweichen',))
                c24.button(label="-1", key=155, on_click=decrement_stat, args=('entweichen',))
                c25.markdown(f'<p class="big-font">Schnelligkeit</p>', unsafe_allow_html=True)
                c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['schnelligkeit']),
                            unsafe_allow_html=True)
                c27.button(label="+1", key=156, on_click=increment_stat, args=('schnelligkeit',))
                c28.button(label="-1", key=157, on_click=decrement_stat, args=('schnelligkeit',))
                c29.markdown(f'<p class="big-font">Überzeugen</p>', unsafe_allow_html=True)
                c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ueberzeugen']),
                             unsafe_allow_html=True)
                c211.button(label="+1", key=158, on_click=increment_stat, args=('ueberzeugen',))
                c212.button(label="-1", key=159, on_click=decrement_stat, args=('ueberzeugen',))
                c213.markdown(f'<p class="big-font">Handwerk</p>', unsafe_allow_html=True)
                c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['handwerk']),
                              unsafe_allow_html=True)
                c215.button(label="+1", key=160, on_click=increment_stat, args=('handwerk',))
                c216.button(label="-1", key=161, on_click=decrement_stat, args=('handwerk',))
            with st.container():
                c21.markdown(f'<p class="big-font">Zähigkeit</p>', unsafe_allow_html=True)
                c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['zähigkeit']),
                            unsafe_allow_html=True)
                c23.button(label="+1", key=162, on_click=increment_stat, args=('zähigkeit',))
                c24.button(label="-1", key=163, on_click=decrement_stat, args=('zähigkeit',))
                c25.markdown(f'<p class="big-font">Nachsetzen</p>', unsafe_allow_html=True)
                c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['nachsetzen']),
                            unsafe_allow_html=True)
                c27.button(label="+1", key=164, on_click=increment_stat, args=('nachsetzen',))
                c28.button(label="-1", key=165, on_click=decrement_stat, args=('nachsetzen',))
                c29.markdown(f'<p class="big-font">Einschüchtern</p>', unsafe_allow_html=True)
                c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['einschuechtern']),
                             unsafe_allow_html=True)
                c211.button(label="+1", key=166, on_click=increment_stat, args=('einschuechtern',))
                c212.button(label="-1", key=167, on_click=decrement_stat, args=('einschuechtern',))
                c213.markdown(f'<p class="big-font">Steuerung</p>', unsafe_allow_html=True)
                c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['steuerung']),
                              unsafe_allow_html=True)
                c215.button(label="+1", key=168, on_click=increment_stat, args=('steuerung',))
                c216.button(label="-1", key=169, on_click=decrement_stat, args=('steuerung',))
        with tab2:
            create_item_elements_for_character_id(st.session_state.active_char["id"])
            st.divider()
            item_names = get_values_alchemy(table_name='items', column_name='name')
            item_to_add = st.selectbox('Add Item', item_names)
            if st.button("Add Item"):
                add_item_to_character(st.session_state.active_char['id'], item_to_add)
                st.toast("Item added to your character", icon="✅")
                time.sleep(1)
                st.experimental_rerun()

        with tab3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

        if st.button('Log Out'):
            st.session_state.logged_in = False
            st.session_state.char_fetched = False
            del st.session_state['active_char']
            st.experimental_rerun()


if __name__ == "__main__":
    app()
