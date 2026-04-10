import streamlit as st
import pandas as pd
from utils.parser import parse_csv

def upload_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div style='text-align:center; margin-bottom:1.5rem;'>
                <h3 style='margin-bottom:0.3rem;'>Upload Bank Statement</h3>
                <p style='color:#94a3b8; font-size:0.9rem; margin-top:0;'>
                    Upload a CSV file with Date, Description, and Amount columns to begin your analysis.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        file = st.file_uploader(
            "Choose CSV file",
            type=["csv"],
            label_visibility="collapsed"
        )

        if file:
            with st.spinner("Analyzing statement..."):
                use_ai = st.session_state.get("use_ai", False)
                df = parse_csv(file, use_ai=use_ai)
                if df is not None:
                    st.success(f"Successfully loaded {len(df)} transactions.")
                    return df
                else:
                    st.error("Could not parse this file. Ensure it has Date, Description, and Amount columns.")

    return None
