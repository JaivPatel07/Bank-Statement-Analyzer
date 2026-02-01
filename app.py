import streamlit as st
from ui.upload import upload_page
from ui.dashboard import dashboard_page

st.set_page_config(page_title="Bank Statement Analyzer", page_icon="💰", layout="wide")
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.title("Secure Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
if not st.session_state.authenticated:
    login_page()
else:
    with st.sidebar:
        st.title("Finance App")
        st.write("Welcome, Admin")
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
    df = upload_page()
    if df is not None:
        st.divider()
        dashboard_page(df)
