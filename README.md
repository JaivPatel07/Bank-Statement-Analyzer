# Bank Statement Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-FF4B4B)

A web-based finance analysis tool built using Streamlit that processes bank statement CSV files and provides insights into spending patterns, income, and financial trends through visualizations and summaries.

---

## Live Demo

Access the application:
https://jaivpatel07-bank-statement-analyzer-app-vhw2kv.streamlit.app/

**Credentials:**
Username: admin
Password: admin

---

## Overview

This project automates the analysis of bank statements by parsing transaction data, cleaning and organizing it, and generating meaningful insights.

It demonstrates:

* Data parsing and transformation
* Financial data analysis
* Visualization of trends and categories
* End-to-end application development

---

## Features

### Data Processing

* Upload CSV bank statements
* Parse and normalize transaction data
* Handle income and expense entries

### Categorization

* Automatically categorize transactions using keyword-based logic
* Supports categories like Food, Bills, Transport, and Income

### Dashboard

* Total income, expenses, and balance
* Category-wise spending (pie chart)
* Income vs expense comparison
* Monthly and daily trends

### Export

* Download cleaned data as CSV
* Generate PDF reports

### Authentication

* Basic login system for controlled access

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib, Plotly
* FPDF

---

## Project Structure

```
Bank-Statement-Analyzer/
│
├── ui/
│   ├── upload.py
│   └── dashboard.py
│
├── utils/
│   ├── parser.py
│   └── exporter.py
│
├── app.py
├── requirements.txt
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
streamlit run app.py
```

---

## Usage

1. Upload a bank statement CSV file
2. View analyzed data and visualizations
3. Explore spending patterns
4. Export reports if needed

---

## Future Improvements

* Advanced categorization using machine learning
* Better UI/UX design
* Secure authentication system
* Support for multiple bank formats

---

## About

This project showcases practical skills in data processing, visualization, and building real-world applications using Python and Streamlit.
