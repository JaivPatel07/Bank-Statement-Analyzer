# FinancePro — Smart Bank Statement Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-FF4B4B)
![AI](https://img.shields.io/badge/Gemini-AI_Powered-4285F4)

A premium, AI-enhanced financial intelligence platform that transforms raw bank statement CSVs into actionable financial insights with interactive dashboards, spending forecasts, and anomaly detection.

---

## Live Demo

Access the application:
https://jaivpatel07-bank-statement-analyzer-app-vhw2kv.streamlit.app/

**Credentials:**
Username: admin
Password: admin

---

## Features

### Financial Intelligence Dashboard
* 5 KPI metric cards (Income, Expenses, Balance, Health Score, Transaction Count)
* Interactive date range filtering
* Financial Health gauge chart (0-100 score)
* Savings rate analysis

### AI-Powered Insights
* Gemini API integration for smart transaction categorization
* Personalized financial advice generation
* Rule-based fallback when API is unavailable
* Anomaly detection for unusual spending patterns

### Advanced Analytics
* Cumulative cash flow visualization
* Linear regression spending forecast (next 30 days)
* Monthly spending trend analysis
* Top merchant identification and ranking

### Merchant Analysis
* Top spending merchants with percentage breakdown
* Horizontal bar chart visualization
* Category-wise spending distribution (donut chart)

### Data & Export
* Full transaction table with category filtering
* PDF report generation with charts and executive summary
* CSV export with cleaned/categorized data

### Authentication
* Secure login system
* Session-based state management
* Multi-currency support ($, ₹, €, £, ¥)

---

## Tech Stack

* **Frontend:** Streamlit, Plotly, Custom CSS
* **Backend:** Python, Pandas, NumPy
* **AI:** Google Gemini API
* **ML:** Scikit-learn (Linear Regression for forecasting)
* **Export:** FPDF, Matplotlib

---

## Project Structure

```
Bank-Statement-Analyzer/
│
├── assets/
│   └── style.css              # Premium dark theme CSS
│
├── ui/
│   ├── upload.py              # File upload
│   └── dashboard.py           # Main dashboard with 5 tabs
│
├── utils/
│   ├── parser.py              # CSV parsing & categorization
│   ├── ai_engine.py           # Gemini AI integration
│   ├── analytics.py           # Health scores & forecasting
│   └── exporter.py            # PDF report generation
│
├── app.py                     # Main application entry point
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md
```

---

## Installation

```bash
git clone https://github.com/JaivPatel07/Bank-Statement-Analyzer.git
cd Bank-Statement-Analyzer

python -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

# Optional: Set up AI features
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

streamlit run app.py
```

---

## Usage

1. Login with `admin` / `admin`
2. Upload a bank statement CSV
3. Explore the 5 dashboard tabs:
   - **Overview** — Pie charts, bar graphs, health gauge
   - **AI Insights** — Financial advice & anomaly alerts
   - **Merchants** — Top spending breakdown
   - **Trends** — Cash flow, forecasts, monthly trends
   - **Data & Export** — Filter, search, export PDF/CSV

---

## CSV Format

Your CSV should have these columns (case-insensitive):

| Column | Description |
|--------|-------------|
| Date | Transaction date (YYYY-MM-DD) |
| Description | Merchant or transaction description |
| Amount | Transaction amount (positive = income, negative = expense) |

---

## About

A comprehensive financial analytics platform showcasing practical skills in data processing, AI integration, machine learning, visualization, and building real-world applications using Python and Streamlit.
