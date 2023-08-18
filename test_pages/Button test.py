from util import *
if 'kk' not in st.session_state:
    st.session_state.kk = 1

st.write(st.session_state.kk)




st.button("+1", on_click=increment_stat,args=('kk',))
st.button("-1", on_click=decrement_stat,args=('kk',))
