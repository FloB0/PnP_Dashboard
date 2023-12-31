from util import *

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
        c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['kk']), unsafe_allow_html=True)
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
        c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['a']), unsafe_allow_html=True)
        c3.button(label="+1", key=106, on_click=increment_stat, args=('a',))
        c4.button(label="-1", key=107, on_click=decrement_stat, args=('a',))
        c5.markdown(f'<p class="big-font">Willenskraft</p>', unsafe_allow_html=True)
        c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wk']), unsafe_allow_html=True)
        c7.button(label="+1", key=108, on_click=increment_stat, args=('wk',))
        c8.button(label="-1", key=109, on_click=decrement_stat, args=('wk',))
        c9.markdown(f'<p class="big-font">Technisches Verständnis</p>', unsafe_allow_html=True)
        c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['tv']), unsafe_allow_html=True)
        c11.button(label="+1", key=110, on_click=increment_stat, args=('tv',))
        c12.button(label="-1", key=111, on_click=decrement_stat, args=('tv',))
    with st.container():
        c1.markdown(f'<p class="big-font">Präzision</p>', unsafe_allow_html=True)
        c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p']), unsafe_allow_html=True)
        c3.button(label="+1", key=112, on_click=increment_stat, args=('p',))
        c4.button(label="-1", key=113, on_click=decrement_stat, args=('p',))
        c5.markdown(f'<p class="big-font">Wahrnehmung</p>', unsafe_allow_html=True)
        c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wa']), unsafe_allow_html=True)
        c7.button(label="+1", key=114, on_click=increment_stat, args=('wa',))
        c8.button(label="-1", key=115, on_click=decrement_stat, args=('wa',))
        c9.markdown(f'<p class="big-font">Glück</p>', unsafe_allow_html=True)
        c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['g']), unsafe_allow_html=True)
        c11.button(label="+1", key=116, on_click=increment_stat, args=('g',))
        c12.button(label="-1", key=117, on_click=decrement_stat, args=('g',))
    with st.container():
        c1.markdown(f'<p class="big-font">Physische Belbarkeitast</p>', unsafe_allow_html=True)
        c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['pb']), unsafe_allow_html=True)
        c3.button(label="+1", key=118, on_click=increment_stat, args=('pb',))
        c4.button(label="-1", key=119, on_click=decrement_stat, args=('pb',))
        c5.markdown(f'<p class="big-font">Mentale Belastbarkeit</p>', unsafe_allow_html=True)
        c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['mb']), unsafe_allow_html=True)
        c7.button(label="+1", key=120, on_click=increment_stat, args=('mb',))
        c8.button(label="-1", key=121, on_click=decrement_stat, args=('mb',))
        c9.markdown(f'<p class="big-font">Wissen</p>', unsafe_allow_html=True)
        c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wi']), unsafe_allow_html=True)
        c11.button(label="+1", key=122, on_click=increment_stat, args=('wi',))
        c12.button(label="-1", key=123, on_click=decrement_stat, args=('wi',))
    with st.container():
        c1.markdown(f'<p class="big-font">Verhindern</p>', unsafe_allow_html=True)
        c2.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['v']), unsafe_allow_html=True)
        c3.button(label="+1", key=124, on_click=increment_stat, args=('v',))
        c4.button(label="-1", key=125, on_click=decrement_stat, args=('v',))
        c5.markdown(f'<p class="big-font">Inspiration</p>', unsafe_allow_html=True)
        c6.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ins']), unsafe_allow_html=True)
        c7.button(label="+1", key=126, on_click=increment_stat, args=('ins',))
        c8.button(label="-1", key=127, on_click=decrement_stat, args=('ins',))
        c9.markdown(f'<p class="big-font">Charisma</p>', unsafe_allow_html=True)
        c10.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['c']), unsafe_allow_html=True)
        c11.button(label="+1", key=128, on_click=increment_stat, args=('c',))
        c12.button(label="-1", key=129, on_click=decrement_stat, args=('c',))
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
