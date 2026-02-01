import streamlit as st
from utils.parser import parse_csv, categorize

def upload_page():
    st.header("Upload Bank Statement")

    file = st.file_uploader("Upload CSV", type=["csv"], help="Upload your bank statement in CSV format")

    if file:
        with st.spinner("Processing file..."):
            df = parse_csv(file)
            if df is not None:
                if "description" in df.columns:
                    df["category"] = df["description"].apply(categorize)
                
                st.success("File processed successfully!")
                return df
    return None
