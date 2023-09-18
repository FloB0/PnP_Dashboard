from sqlalchemy import create_engine
import streamlit as st

DATABASE_URI = f"mysql+mysqlconnector://{st.secrets['MYSQL']['USERNAME']}:{st.secrets['MYSQL']['PASSWORD']}@{st.secrets['MYSQL']['SERVER']}/{st.secrets['MYSQL']['DATABASE']}"


@st.cache_resource
def init_connection_alchemy():
    engine = create_engine(DATABASE_URI)
    return engine

print(init_connection_alchemy())