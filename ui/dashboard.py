import streamlit as st
import pandas as pd
import plotly.express as px
from utils.exporter import generate_pdf


def dashboard_page(df):
    st.title("Finance Dashboard")
    st.markdown("Analyze income, expenses, and spending patterns from bank statements.")

    if df is None or df.empty:
        st.info("Upload a CSV file to begin analysis")
        return

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    with st.container():
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", min_date)
        end_date = col2.date_input("End Date", max_date)

    if start_date > end_date:
        st.error("Start date must be before end date")
        return

    df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

    income = df[df["category"] == "Income"]["amount"].sum()
    expenses = abs(df[df["category"] != "Income"]["amount"].sum())
    balance = income - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${income:,.2f}", delta="Credit")
    col2.metric("Expenses", f"${expenses:,.2f}", delta="-Debit", delta_color="inverse")
    col3.metric("Balance", f"${balance:,.2f}")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Overview", "Trends", "Data & Export"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            spending = df[df["category"] != "Income"]

            if not spending.empty:
                by_cat = (
                    spending.groupby("category")["amount"].sum()
                    .abs()
                    .reset_index()
                )
                fig = px.pie(
                    by_cat,
                    values="amount",
                    names="category",
                    hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(margin=dict(t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data available")

        with col2:
            st.subheader("Income vs Expense")

            comp_df = pd.DataFrame({
                "Type": ["Income", "Expense"],
                "Amount": [income, expenses]
            })

            fig = px.bar(
                comp_df,
                x="Type",
                y="Amount",
                color="Type",
                color_discrete_map={
                    "Income": "#2ecc71",
                    "Expense": "#e74c3c"
                },
                text_auto='.2s'
            )
            fig.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Monthly Trend")
            trend = (
                df.groupby(df["date"].dt.to_period("M"))["amount"]
                .sum()
                .reset_index()
            )
            trend["date"] = trend["date"].astype(str)

            fig = px.line(
                trend,
                x="date",
                y="amount",
                markers=True,
                title="Net Balance Trend"
            )
            fig.update_layout(margin=dict(t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Daily Spending Trend")
            categories = ["All"] + list(
                df[df["category"] != "Income"]["category"].unique()
            )
            selected_category = st.selectbox("Filter Category", categories)

            daily_expenses = df[df["category"] != "Income"]
            if selected_category != "All":
                daily_expenses = daily_expenses[
                    daily_expenses["category"] == selected_category
                ]

            daily_trend = (
                daily_expenses
                .groupby(daily_expenses["date"].dt.date)["amount"]
                .sum()
                .abs()
                .reset_index()
            )

            if daily_trend.empty:
                st.info("No transactions available")
            else:
                fig = px.bar(daily_trend, x="date", y="amount")
                fig.update_layout(margin=dict(t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.subheader("Export")
            st.download_button(
                "Download PDF",
                data=generate_pdf(df),
                file_name="transaction_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name="transactions.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            st.subheader("Recent Transactions")
            st.dataframe(
                df.sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True
            )
