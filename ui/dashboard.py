from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.exporter import generate_pdf
from utils.analytics import calculate_health_score, get_top_merchants, forecast_spending
from utils.ai_engine import get_financial_advice, detect_anomalies

def render_health_gauge(score):
    if score >= 70:
        color = "#10b981"
        label = "Excellent"
    elif score >= 40:
        color = "#f59e0b"
        label = "Average"
    else:
        color = "#ef4444"
        label = "Needs Attention"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': label, 'font': {'size': 14, 'color': '#94a3b8'}},
        number={'font': {'size': 40, 'color': color}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#334155'},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': '#1e293b',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239,68,68,0.1)'},
                {'range': [40, 70], 'color': 'rgba(245,158,11,0.1)'},
                {'range': [70, 100], 'color': 'rgba(16,185,129,0.1)'}
            ],
        }
    ))
    fig.update_layout(
        height=200, margin=dict(t=30, b=0, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0'
    )
    return fig

def dashboard_page(df):
    symbol = st.session_state.get("currency", "$")

    st.markdown("""
        <h2 style='margin-bottom:0;'>Financial Intelligence Dashboard</h2>
        <p style='color:#64748b; margin-top:0.2rem;'>Real-time analysis of your spending patterns</p>
    """, unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("Upload a CSV file to begin analysis.")
        return

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    st.markdown("")
    fc1, fc2, fc3 = st.columns([1, 1, 2.5])
    with fc1:
        start_date = st.date_input("From", df["date"].min().date())
    with fc2:
        end_date = st.date_input("To", df["date"].max().date())

    if start_date > end_date:
        st.error("Start date must be before end date.")
        return

    filtered_df = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date)
    ].copy()

    if filtered_df.empty:
        st.warning("No transactions found in selected date range.")
        return

    income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
    expenses = abs(filtered_df[filtered_df["category"] != "Income"]["amount"].sum())
    balance = income - expenses
    health_score = calculate_health_score(filtered_df)
    txn_count = len(filtered_df)

    st.markdown("")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Income", f"{symbol}{income:,.0f}")
    m2.metric("Expenses", f"{symbol}{expenses:,.0f}")
    m3.metric("Balance", f"{symbol}{balance:,.0f}")
    m4.metric("Health Score", f"{health_score}/100")
    m5.metric("Transactions", f"{txn_count}")

    st.markdown("")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", "AI Insights", "Merchants", "Trends", "Data & Export"
    ])

    with tab1:
        ov1, ov2, ov3 = st.columns([1.2, 1, 1])

        with ov1:
            st.markdown("##### Spending by Category")
            spending = filtered_df[filtered_df["category"] != "Income"]
            if not spending.empty:
                by_cat = spending.groupby("category")["amount"].sum().abs().reset_index()
                by_cat = by_cat.sort_values("amount", ascending=False)
                fig = px.pie(
                    by_cat, values="amount", names="category", hole=0.55,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(
                    height=350, margin=dict(t=20, b=20, l=10, r=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    legend=dict(font=dict(size=11))
                )
                fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=10)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data available.")

        with ov2:
            st.markdown("##### Income vs Expenses")
            comp_df = pd.DataFrame({
                "Type": ["Income", "Expenses"],
                "Amount": [income, expenses]
            })
            fig = px.bar(
                comp_df, x="Type", y="Amount", color="Type",
                color_discrete_map={"Income": "#10b981", "Expenses": "#ef4444"},
                text_auto='.2s'
            )
            fig.update_layout(
                height=350, showlegend=False,
                margin=dict(t=20, b=20), paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0',
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)

        with ov3:
            st.markdown("##### Financial Health")
            fig = render_health_gauge(health_score)
            st.plotly_chart(fig, use_container_width=True)

            savings_rate = ((income - expenses) / income * 100) if income > 0 else 0
            st.markdown(f"""
                <div style='background:rgba(99,102,241,0.06); padding:1rem; border-radius:12px; margin-top:0.5rem;'>
                    <p style='margin:0; font-size:0.85rem; color:#94a3b8;'>Savings Rate</p>
                    <p style='margin:0; font-size:1.3rem; font-weight:700; color:{"#10b981" if savings_rate > 0 else "#ef4444"};'>
                        {savings_rate:.1f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        ai1, ai2 = st.columns([1.5, 1])

        with ai1:
            st.markdown("##### Financial Advice")
            summary = {
                "income": float(income),
                "expenses": float(expenses),
                "savings_rate": float(savings_rate) if income > 0 else 0,
                "top_categories": {
                    k: float(v) for k, v in
                    filtered_df[filtered_df["category"] != "Income"]
                    .groupby("category")["amount"].sum().abs()
                    .sort_values(ascending=False).head(5).to_dict().items()
                }
            }
            advice = get_financial_advice(summary)

            st.markdown(f"""
                <div style='background:linear-gradient(135deg, rgba(99,102,241,0.08), rgba(16,185,129,0.05));
                            padding:1.5rem; border-radius:16px; border-left:4px solid #6366f1;
                            line-height:1.7; font-size:0.95rem;'>
                    {advice}
                </div>
            """, unsafe_allow_html=True)

        with ai2:
            st.markdown("##### Anomaly Detection")
            anomalies = detect_anomalies(filtered_df)
            if anomalies:
                for a in anomalies[:5]:
                    amt = abs(a['amount'])
                    st.markdown(f"""
                        <div style='background:rgba(239,68,68,0.08); padding:0.8rem 1rem; 
                                    border-radius:10px; margin-bottom:0.5rem; border-left:3px solid #ef4444;'>
                            <strong>{a['description']}</strong><br>
                            <span style='color:#ef4444; font-weight:600;'>{symbol}{amt:,.0f}</span>
                            <span style='color:#94a3b8; font-size:0.8rem;'> — {a['reason']}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background:rgba(16,185,129,0.08); padding:1.2rem; border-radius:12px; text-align:center;'>
                        <p style='color:#10b981; font-weight:600; margin:0.5rem 0 0;'>All Clear!</p>
                        <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>No unusual spending patterns detected.</p>
                    </div>
                """, unsafe_allow_html=True)

    with tab3:
        mc1, mc2 = st.columns([1, 1.5])

        with mc1:
            st.markdown("##### Top Spending Merchants")
            top_m = get_top_merchants(filtered_df, top_n=8)
            if not top_m.empty:
                for i, (_, row) in enumerate(top_m.iterrows()):
                    pct = (row['amount'] / expenses * 100) if expenses > 0 else 0
                    st.markdown(f"""
                        <div style='display:flex; justify-content:space-between; align-items:center;
                                    padding:0.6rem 0.8rem; border-radius:8px; margin-bottom:4px;
                                    background:rgba(99,102,241,{0.06 + i*0.01});'>
                            <span>
                                <strong>{row['description']}</strong>
                                <span style='color:#64748b; font-size:0.78rem; margin-left:0.5rem;'>{pct:.1f}%</span>
                            </span>
                            <span style='font-weight:700; color:#f1f5f9;'>{symbol}{row['amount']:,.0f}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No merchant data found.")

        with mc2:
            st.markdown("##### Merchant Breakdown")
            if not top_m.empty:
                fig = px.bar(
                    top_m, y="description", x="amount", orientation='h',
                    color="amount",
                    color_continuous_scale=["#818cf8", "#6366f1", "#4f46e5"],
                )
                fig.update_layout(
                    height=400, showlegend=False, coloraxis_showscale=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    yaxis={'categoryorder': 'total ascending'},
                    xaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        tr1, tr2 = st.columns(2)

        with tr1:
            st.markdown("##### Cumulative Cash Flow")
            daily = filtered_df.groupby(filtered_df["date"].dt.date)["amount"].sum().reset_index()
            daily['cumulative'] = daily['amount'].cumsum()
            fig = px.area(daily, x="date", y="cumulative")
            fig.update_traces(
                fill='tozeroy',
                fillcolor='rgba(99,102,241,0.15)',
                line_color='#6366f1'
            )
            fig.update_layout(
                height=400, margin=dict(t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e2e8f0',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)

        with tr2:
            st.markdown("##### Spending Forecast")
            forecast_val, forecast_data = forecast_spending(filtered_df)

            st.markdown(f"""
                <div style='text-align:center; padding:1.5rem; background:linear-gradient(135deg, rgba(99,102,241,0.1), rgba(16,185,129,0.05));
                            border-radius:16px; border:1px solid rgba(99,102,241,0.2);'>
                    <p style='color:#94a3b8; font-size:0.85rem; margin:0;'>Projected Next 30 Days</p>
                    <h2 style='color:#a5b4fc; margin:0.5rem 0; font-size:2.2rem;'>{symbol}{forecast_val:,.0f}</h2>
                    <p style='font-size:0.8rem; color:#10b981; margin:0;'>Linear regression analysis</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            st.markdown("##### Monthly Spending Trend")
            monthly = filtered_df[filtered_df["category"] != "Income"].copy()
            if not monthly.empty:
                monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
                monthly_sum = monthly.groupby("month")["amount"].sum().abs().reset_index()
                fig = px.bar(monthly_sum, x="month", y="amount", color_discrete_sequence=["#818cf8"])
                fig.update_layout(
                    height=250, margin=dict(t=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(99,102,241,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab5:
        ex1, ex2 = st.columns([1, 3])

        with ex1:
            st.markdown("##### Export Options")
            
            try:
                pdf_data = generate_pdf(filtered_df)
                st.download_button(
                    "Download PDF Report",
                    data=pdf_data,
                    file_name=f"Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF error: {e}")

            st.download_button(
                "Download CSV",
                data=filtered_df.to_csv(index=False),
                file_name=f"Data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("")
            st.markdown(f"""
                <div style='background:rgba(99,102,241,0.06); padding:1rem; border-radius:12px;'>
                    <p style='color:#94a3b8; font-size:0.78rem; margin:0;'>SUMMARY</p>
                    <p style='margin:0.3rem 0 0; font-size:0.9rem;'>{len(filtered_df)} rows</p>
                    <p style='margin:0.2rem 0 0; font-size:0.9rem;'>{filtered_df['category'].nunique()} categories</p>
                </div>
            """, unsafe_allow_html=True)

        with ex2:
            st.markdown("##### All Transactions")

            cats = ["All"] + sorted(filtered_df["category"].unique().tolist())
            selected_cat = st.selectbox("Category Filter", cats, label_visibility="collapsed")

            display_df = filtered_df.copy()
            if selected_cat != "All":
                display_df = display_df[display_df["category"] == selected_cat]

            display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(
                display_df.sort_values("date", ascending=False)[["date", "description", "amount", "category"]],
                use_container_width=True,
                hide_index=True,
                height=500
            )
