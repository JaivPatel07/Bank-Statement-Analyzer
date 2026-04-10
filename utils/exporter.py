from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import os
import pandas as pd
from datetime import datetime


class ReportPDF(FPDF):
    def header(self):
        self.set_fill_color(99, 102, 241)
        self.rect(0, 0, 210, 35, 'F')

        self.set_font('Arial', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 18, 'FINANCEPRO REPORT', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()} | FinancePro Analysis', 0, 0, 'C')


def generate_pdf(df: pd.DataFrame) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    income = df[df["category"] == "Income"]["amount"].sum()
    expenses = abs(df[df["category"] != "Income"]["amount"].sum())
    balance = income - expenses
    savings_pct = ((income - expenses) / income * 100) if income > 0 else 0

    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Financial Summary", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(240, 245, 255)
    pdf.cell(45, 15, f"Income: {income:,.0f}", 1, 0, 'C', 1)
    pdf.cell(45, 15, f"Expenses: {expenses:,.0f}", 1, 0, 'C', 1)
    pdf.cell(45, 15, f"Balance: {balance:,.0f}", 1, 0, 'C', 1)
    pdf.cell(45, 15, f"Savings: {savings_pct:.1f}%", 1, 1, 'C', 1)
    pdf.ln(8)

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "Transaction Log", ln=True)
    pdf.ln(3)

    pdf.set_fill_color(99, 102, 241)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(28, 9, "Date", 1, 0, 'C', 1)
    pdf.cell(75, 9, "Description", 1, 0, 'C', 1)
    pdf.cell(30, 9, "Amount", 1, 0, 'C', 1)
    pdf.cell(35, 9, "Category", 1, 1, 'C', 1)

    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Arial", size=8)
    fill = False
    row_count = 0
    max_rows = 500

    for _, row in df.iterrows():
        if row_count >= max_rows:
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(168, 9, f"... and {len(df) - max_rows} more rows", 1, 1, 'C')
            break

        if fill:
            pdf.set_fill_color(241, 245, 249)
        else:
            pdf.set_fill_color(255, 255, 255)

        try:
            date_str = row["date"].strftime("%Y-%m-%d")
        except Exception:
            date_str = str(row["date"])[:10]

        desc = str(row.get("description", ""))[:38]
        amt = f"{row['amount']:,.2f}"
        cat = str(row.get('category', 'N/A'))

        pdf.cell(28, 7, date_str, 1, 0, 'C', 1)
        pdf.cell(75, 7, desc, 1, 0, 'L', 1)
        pdf.cell(30, 7, amt, 1, 0, 'R', 1)
        pdf.cell(35, 7, cat, 1, 1, 'C', 1)
        fill = not fill
        row_count += 1

    expenses_df = df[df["category"] != "Income"]
    if not expenses_df.empty:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 10, "Expense Analysis", ln=True, align='C')
        summary = expenses_df.groupby("category")["amount"].sum().abs().sort_values(ascending=False)

        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = plt.cm.Set3(range(len(summary)))
        wedges, texts, autotexts = ax.pie(
            summary, labels=summary.index, autopct='%1.1f%%',
            colors=colors, startangle=140
        )
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(8)
        ax.set_title("Spending Distribution by Category", fontsize=12, fontweight='bold')
        plt.tight_layout()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            plt.savefig(tmp.name, dpi=150, bbox_inches='tight', facecolor='white')
            pdf.image(tmp.name, x=15, w=180)

        plt.close()
        os.remove(tmp.name)

    return pdf.output(dest='S').encode('latin-1')
