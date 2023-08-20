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
styl = f"""
<style>
.bottom_text {{
    position: fixed;
    bottom: 3rem;
}}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

from util import (get_values_alchemy, get_character_by_name_alchemy, increment_stat, decrement_stat)
import time


def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Character Dashboard")
        names_from_primary_info = get_values_alchemy('primary_info', 'name')
        st.session_state.key = st.selectbox("Select your character", names_from_primary_info)
        if st.button('Log in'):
            character = get_character_by_name_alchemy(st.session_state.key)
            st.session_state.active_char = character
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
            st.experimental_rerun()
        else:
            if 'active_char' not in st.session_state:
                st.toast("Character is not valid anymore", icon="🚨")
                st.session_state.logged_in = False
                st.session_state.char_fetched = False
                time.sleep(2)
                st.experimental_rerun()
            # The user is logged in
            st.title(f"Primary Abilities - {st.session_state['active_char']['name']}")
            st.divider()
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
            # st.markdown(f'<p class="bottom_text">Some text</p>', unsafe_allow_html=True)
        st.divider()
        # c41, c42, c43 = st.columns([20, 1.5, 1.5])

        # with c42:
        if 'active_char' in st.session_state:
            if st.session_state.active_char != get_character_by_name_alchemy(st.session_state.key):
                if st.button("Reset", type= "primary"):
                    print("3")
        # with c43:
        if 'active_char' in st.session_state:
            if st.session_state.active_char != get_character_by_name_alchemy(st.session_state.key):
                if st.button("Update", type= "primary"):
                    print("3")
        # with c41:
        if st.button('Log Out'):
            st.session_state.logged_in = False
            st.session_state.char_fetched = False
            del st.session_state['active_char']
            st.experimental_rerun()


if __name__ == "__main__":
    app()
