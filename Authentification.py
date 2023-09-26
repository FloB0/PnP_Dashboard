import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import os
from util import check_user_admin

COURIER_AUTH_TOKEN = os.environ.get("COURIER_AUTH_TOKEN")


if __name__ == "__main__":
    __login__obj = __login__(auth_token=COURIER_AUTH_TOKEN,
                             company_name="DarkDystopia",
                             width=200, height=250,
                             logout_button_name='Logout', hide_menu_bool=False ,
                             hide_footer_bool=True,
                             lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()
    st.session_state.USERNAME = __login__obj.cookies["__streamlit_login_signup_ui_username__"]
    st.session_state.ADMIN = check_user_admin(st.session_state.USERNAME)
    if LOGGED_IN == True:
        st.session_state.LOGGED_IN = True
        if 'AUTHENTICATED' not in st.session_state:
            st.session_state.AUTHENTICATED = False
    else:
        st.session_state.LOGGED_IN = False
        st.session_state.AUTHENTICATED = False