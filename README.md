# 💰 Bank Statement Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-FF4B4B)

A simple **student-built finance analyzer** made with Streamlit that helps you understand your spending by analyzing bank statement CSV files.  
It turns raw transaction data into easy charts and summaries so you can see where your money goes.

---

## 🚀 Live Demonstration

Experience the application in real-time: [**Launch Bank Statement Analyzer**](https://jaivpatel07-bank-statement-analyzer-app-vhw2kv.streamlit.app/)

**Access Credentials:**
- **Username:** `admin`
- **Password:** `admin`

---

## 📌 Project Overview

The **Bank Statement Analyzer** addresses the need for efficient personal finance tracking by automating the processing of bank transaction records. By leveraging data processing algorithms, the application parses raw CSV statements, normalizes date formats, and categorizes transactions to provide a clear financial picture.

**Core Competencies Demonstrated:**
- **Data Engineering:** Robust parsing and cleaning of financial datasets.
- **Financial Analytics:** Automated calculation of income, expenses, and net balance.
- **Data Visualization:** Dynamic charts for trend analysis and category breakdowns.
- **Full-Stack Logic:** End-to-end implementation using Python and Streamlit.

---

## ✨ Features

### 📂 Upload & Analyze
- Upload your bank statement as CSV  
- Automatically reads and sorts transactions  
- Supports income (+) and expenses (-)

### 🏷️ Auto Categorization
- Uses keywords in descriptions  
- Categories like Food, Bills, Transport, Income, etc.  
- Basic but works well for common cases

### 📊 Dashboard
- Total income, expenses, and balance  
- Spending by category (pie chart)  
- Income vs expense comparison  
- Monthly and daily trends

### 📄 Export
- Download cleaned data as CSV  
- Generate a PDF report

### 🔐 Simple Login
- Basic login added for practice  
- Not meant for real security

---

## 🛠️ Technical Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.8+ | Core logic and scripting |
| **Framework** | Streamlit | Web application interface and state management |
| **Data Manipulation** | Pandas | Dataframes, cleaning, and aggregation |
| **Visualization** | Plotly & Matplotlib | Interactive and static charting |
| **Reporting** | FPDF | PDF report generation |

---

## � Project Structure

```text
Bank-Statement-Analyzer/
│
├── ui/
│   ├── upload.py       # File upload and validation interface
│   └── dashboard.py    # Visualization logic and dashboard layout
│
├── utils/
│   ├── parser.py       # Core logic for parsing and categorizing transactions
│   └── exporter.py     # PDF generation and CSV export utilities
│
├── app.py              # Application entry point
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 🛠️ Built With

- Python  
- Streamlit  
- Pandas  
- Plotly  
- Matplotlib  
- FPDF  

---

---

## ⚙️ Installation & Setup

Follow these steps to set up the project locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/bank-statement-analyzer.git
cd bank-statement-analyzer
```

### 2️⃣ Environment Setup

Create a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🚀 Usage Guide

1. **Launch the App**: Run the command above to start the local server.
2. **Upload Statement**: Drag and drop your bank statement CSV file.
   - *Note: Ensure your CSV has columns for Date, Description, and Amount.*
3. **Analyze**: Explore the interactive charts and summaries.
4. **Download Reports**: Generate a PDF summary or export cleaned data.

---