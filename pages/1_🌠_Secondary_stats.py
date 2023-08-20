import streamlit as st
from util import increment_stat, decrement_stat


st.set_page_config(
        page_title="DarkDystopia",
        page_icon="🌠",
        layout="wide",
    )
st.markdown("""
<style>
.big-font {
    font-size:24.5px !important;
}
</style>
""", unsafe_allow_html=True)

if "active_char" in st.session_state:
    st.title(f"Secondary Abilities - {st.session_state['active_char']['name']}")
    st.divider()
    c101, c111, c121, c131 = st.columns(4)
    c21, c22, c23, c24, c25, c26, c27, c28, c29, c210, c211, c212, c213, c214, c215, c216 = st.columns(
        [3, 2, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1])
    with st.container():
        c101.markdown(f'<p class="big-font">Gefecht</p>', unsafe_allow_html=True)
        c111.markdown(f'<p class="big-font">Gewandtheit</p>', unsafe_allow_html=True)
        c121.markdown(f'<p class="big-font">Gesellschaft</p>', unsafe_allow_html=True)
        c131.markdown(f'<p class="big-font">Wissen</p>', unsafe_allow_html=True)
    with st.container():
        c21.markdown(f'<p class="big-font">Nahkampf</p>', unsafe_allow_html=True)
        c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['kk'] * 2 +
                                                         st.session_state['active_char']['p'] +
                                                         st.session_state['active_char']['nahkampf']),
                     unsafe_allow_html=True)
        c23.button(label="+1", key=130, on_click=increment_stat, args=('nahkampf',))
        c24.button(label="-1", key=131, on_click=decrement_stat, args=('nahkampf',))
        c25.markdown(f'<p class="big-font">Ausweichen</p>', unsafe_allow_html=True)
        c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['v'] +
                                                         st.session_state['active_char']['wa'] +
                                                         st.session_state['active_char']['g'] +
                                                         st.session_state['active_char']['ausweichen']),
                     unsafe_allow_html=True)
        c27.button(label="+1", key=132, on_click=increment_stat, args=('ausweichen',))
        c28.button(label="-1", key=133, on_click=decrement_stat, args=('ausweichen',))
        c29.markdown(f'<p class="big-font">Lügen</p>', unsafe_allow_html=True)
        c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['mb'] +
                                                          st.session_state['active_char']['c'] * 2 +
                                                          st.session_state['active_char']['luegen']),
                      unsafe_allow_html=True)
        c211.button(label="+1", key=134, on_click=increment_stat, args=('luegen',))
        c212.button(label="-1", key=135, on_click=decrement_stat, args=('luegen',))
        c213.markdown(f'<p class="big-font">Mechanik</p>', unsafe_allow_html=True)
        c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['tv'] * 2 +
                                                          st.session_state['active_char']['wi'] +
                                                          st.session_state['active_char']['mechanik']),
                      unsafe_allow_html=True)
        c215.button(label="+1", key=136, on_click=increment_stat, args=('mechanik',))
        c216.button(label="-1", key=137, on_click=decrement_stat, args=('mechanik',))
    with st.container():
        c21.markdown(f'<p class="big-font">Fermkampf</p>', unsafe_allow_html=True)
        c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p'] +
                                                         st.session_state['active_char']['wa'] +
                                                         st.session_state['active_char']['mb'] +
                                                         st.session_state['active_char']['fernkampf']),
                     unsafe_allow_html=True)
        c23.button(label="+1", key=138, on_click=increment_stat, args=('fernkampf',))
        c24.button(label="-1", key=139, on_click=decrement_stat, args=('fernkampf',))
        c25.markdown(f'<p class="big-font">Tarnung</p>', unsafe_allow_html=True)
        c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['pb'] +
                                                         st.session_state['active_char']['g'] +
                                                         st.session_state['active_char']['mb'] +
                                                         st.session_state['active_char']['tarnung']),
                     unsafe_allow_html=True)
        c27.button(label="+1", key=140, on_click=increment_stat, args=('tarnung',))
        c28.button(label="-1", key=141, on_click=decrement_stat, args=('tarnung',))
        c29.markdown(f'<p class="big-font">Etikette</p>', unsafe_allow_html=True)
        c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['ins'] +
                                                          st.session_state['active_char']['wi'] +
                                                          st.session_state['active_char']['c'] +
                                                          st.session_state['active_char']['etikette']),
                      unsafe_allow_html=True)
        c211.button(label="+1", key=142, on_click=increment_stat, args=('etikette',))
        c212.button(label="-1", key=143, on_click=decrement_stat, args=('etikette',))
        c213.markdown(f'<p class="big-font">Ätherkunde</p>', unsafe_allow_html=True)
        c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['mb'] +
                                                          st.session_state['active_char']['intel'] +
                                                          st.session_state['active_char']['wi'] +
                                                          st.session_state['active_char']['aetherkunde']),
                      unsafe_allow_html=True)
        c215.button(label="+1", key=144, on_click=increment_stat, args=('aetherkunde',))
        c216.button(label="-1", key=145, on_click=decrement_stat, args=('aetherkunde',))
    with st.container():
        c21.markdown(f'<p class="big-font">Parieren</p>', unsafe_allow_html=True)
        c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['kk'] +
                                                         st.session_state['active_char']['v'] +
                                                         st.session_state['active_char']['a'] +
                                                         st.session_state['active_char']['parieren']),
                     unsafe_allow_html=True)
        c23.button(label="+1", key=146, on_click=increment_stat, args=('parieren',))
        c24.button(label="-1", key=147, on_click=decrement_stat, args=('parieren',))
        c25.markdown(f'<p class="big-font">Fingerfertigkeit</p>', unsafe_allow_html=True)
        c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p'] +
                                                         st.session_state['active_char']['mb'] +
                                                         st.session_state['active_char']['tv'] +
                                                         st.session_state['active_char']['fingerfertigkeit']),
                     unsafe_allow_html=True)
        c27.button(label="+1", key=148, on_click=increment_stat, args=('fingerfertigkeit',))
        c28.button(label="-1", key=149, on_click=decrement_stat, args=('fingerfertigkeit',))
        c29.markdown(f'<p class="big-font">Handeln</p>', unsafe_allow_html=True)
        c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['intel'] * 2 +
                                                          st.session_state['active_char']['g'] +
                                                          st.session_state['active_char']['handeln']),
                      unsafe_allow_html=True)
        c211.button(label="+1", key=150, on_click=increment_stat, args=('handeln',))
        c212.button(label="-1", key=151, on_click=decrement_stat, args=('handeln',))
        c213.markdown(f'<p class="big-font">Xenos</p>', unsafe_allow_html=True)
        c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['intel'] +
                                                          st.session_state['active_char']['wi'] * 2 +
                                                          st.session_state['active_char']['xenos']),
                      unsafe_allow_html=True)
        c215.button(label="+1", key=152, on_click=increment_stat, args=('xenos',))
        c216.button(label="-1", key=153, on_click=decrement_stat, args=('xenos',))
    with st.container():
        c21.markdown(f'<p class="big-font">Entweichen</p>', unsafe_allow_html=True)
        c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['v'] * 2 +
                                                         st.session_state['active_char']['g'] +
                                                         st.session_state['active_char']['entweichen']),
                     unsafe_allow_html=True)
        c23.button(label="+1", key=154, on_click=increment_stat, args=('entweichen',))
        c24.button(label="-1", key=155, on_click=decrement_stat, args=('entweichen',))
        c25.markdown(f'<p class="big-font">Schnelligkeit</p>', unsafe_allow_html=True)
        c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p'] +
                                                         st.session_state['active_char']['ini'] * 2 +
                                                         st.session_state['active_char']['schnelligkeit']),
                     unsafe_allow_html=True)
        c27.button(label="+1", key=156, on_click=increment_stat, args=('schnelligkeit',))
        c28.button(label="-1", key=157, on_click=decrement_stat, args=('schnelligkeit',))
        c29.markdown(f'<p class="big-font">Überzeugen</p>', unsafe_allow_html=True)
        c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['wk'] * 2 +
                                                          st.session_state['active_char']['ins'] +
                                                          st.session_state['active_char']['ueberzeugen']),
                      unsafe_allow_html=True)
        c211.button(label="+1", key=158, on_click=increment_stat, args=('ueberzeugen',))
        c212.button(label="-1", key=159, on_click=decrement_stat, args=('ueberzeugen',))
        c213.markdown(f'<p class="big-font">Handwerk</p>', unsafe_allow_html=True)
        c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['p'] +
                                                          st.session_state['active_char']['tv'] * 2 +
                                                          st.session_state['active_char']['handwerk']),
                      unsafe_allow_html=True)
        c215.button(label="+1", key=160, on_click=increment_stat, args=('handwerk',))
        c216.button(label="-1", key=161, on_click=decrement_stat, args=('handwerk',))
    with st.container():
        c21.markdown(f'<p class="big-font">Zähigkeit</p>', unsafe_allow_html=True)
        c22.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['a'] * 2 +
                                                         st.session_state['active_char']['pb'] +
                                                         st.session_state['active_char']['zähigkeit']),
                     unsafe_allow_html=True)
        c23.button(label="+1", key=162, on_click=increment_stat, args=('zähigkeit',))
        c24.button(label="-1", key=163, on_click=decrement_stat, args=('zähigkeit',))
        c25.markdown(f'<p class="big-font">Nachsetzen</p>', unsafe_allow_html=True)
        c26.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['v'] +
                                                         st.session_state['active_char']['wk'] +
                                                         st.session_state['active_char']['ini'] +
                                                         st.session_state['active_char']['nachsetzen']),
                     unsafe_allow_html=True)
        c27.button(label="+1", key=164, on_click=increment_stat, args=('nachsetzen',))
        c28.button(label="-1", key=165, on_click=decrement_stat, args=('nachsetzen',))
        c29.markdown(f'<p class="big-font">Einschüchtern</p>', unsafe_allow_html=True)
        c210.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['kk'] +
                                                          st.session_state['active_char']['a'] +
                                                          st.session_state['active_char']['c'] +
                                                          st.session_state['active_char']['einschuechtern']),
                      unsafe_allow_html=True)
        c211.button(label="+1", key=166, on_click=increment_stat, args=('einschuechtern',))
        c212.button(label="-1", key=167, on_click=decrement_stat, args=('einschuechtern',))
        c213.markdown(f'<p class="big-font">Steuerung</p>', unsafe_allow_html=True)
        c214.markdown('<p class="big-font">{}</p>'.format(st.session_state['active_char']['pb'] +
                                                          st.session_state['active_char']['tv'] +
                                                          st.session_state['active_char']['wi'] +
                                                          st.session_state['active_char']['steuerung']),
                      unsafe_allow_html=True)
        c215.button(label="+1", key=168, on_click=increment_stat, args=('steuerung',))
        c216.button(label="-1", key=169, on_click=decrement_stat, args=('steuerung',))

else:
    st.subheader("No character selected")
    st.write("Please log into a character you want to play.")
