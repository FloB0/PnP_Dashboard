import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import os

COURIER_AUTH_TOKEN = os.environ.get("COURIER_AUTH_TOKEN")

if __name__ == "__main__":
    __login__obj = __login__(auth_token=COURIER_AUTH_TOKEN,
                             company_name="DarkDystopia",
                             width=200, height=250,
                             logout_button_name='Logout', hide_menu_bool=False ,
                             hide_footer_bool=True,
                             lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()
    print(__login__obj.__getattribute__())
    if LOGGED_IN == True:
        st.session_state.LOGGED_IN = True
    else:
        st.session_state.LOGGED_IN = False