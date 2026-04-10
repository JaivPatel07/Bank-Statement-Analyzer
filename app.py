import streamlit as st
import os
from ui.upload import upload_page
from ui.dashboard import dashboard_page
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="FinancePro",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "currency" not in st.session_state:
    st.session_state.currency = os.getenv("DEFAULT_CURRENCY", "$")
if "use_ai" not in st.session_state:
    st.session_state.use_ai = False
if "df" not in st.session_state:
    st.session_state.df = None

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
            <div style='text-align:center; margin-bottom:1.5rem;'>
                <h1 style='margin:0; font-size:2rem; 
                    background: linear-gradient(135deg, #6366f1, #a5b4fc);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    FinancePro
                </h1>
                <p style='color:#94a3b8; font-size:0.95rem;'>
                    Intelligent Bank Statement Analysis
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Access Dashboard", use_container_width=True)

            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Use admin / admin")
        
        st.markdown("""
            <p style='text-align:center; color:#475569; font-size:0.8rem; margin-top:1rem;'>
                Demo credentials: admin / admin
            </p>
        """, unsafe_allow_html=True)


if not st.session_state.authenticated:
    login_page()
else:
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center; padding:1rem 0;'>
                <h2 style='margin:0; font-size:1.4rem;
                    background: linear-gradient(135deg, #6366f1, #a5b4fc);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    FinancePro
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown(f"Welcome back, **Admin**")
        st.divider()

        st.markdown("##### Settings")
        st.session_state.currency = st.selectbox(
            "Currency Symbol",
            ["$", "₹", "€", "£", "¥"],
            index=["$", "₹", "€", "£", "¥"].index(st.session_state.currency)
        )

        st.session_state.use_ai = st.toggle(
            "AI Categorization",
            value=st.session_state.use_ai,
            help="Uses Gemini API for categorization. Requires API key in .env"
        )

        st.divider()
        
        if st.session_state.df is not None:
            df_stats = st.session_state.df
            txn_count = len(df_stats)
            cat_count = df_stats['category'].nunique()
            st.markdown(f"""
                <div style='background: rgba(99,102,241,0.08); padding:1rem; border-radius:12px; margin-bottom:1rem;'>
                    <p style='color:#94a3b8; font-size:0.75rem; margin:0;'>DATA SUMMARY</p>
                    <p style='margin:0.3rem 0 0; font-size:0.95rem;'><strong>{txn_count}</strong> transactions</p>
                    <p style='margin:0.2rem 0 0; font-size:0.95rem;'><strong>{cat_count}</strong> categories</p>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.df = None
            st.rerun()

    df = upload_page()
    if df is not None:
        st.session_state.df = df

    if st.session_state.df is not None:
        dashboard_page(st.session_state.df)
