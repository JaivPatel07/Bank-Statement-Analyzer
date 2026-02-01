from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')   # MUST be before pyplot
import matplotlib.pyplot as plt
import tempfile
import os

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Bank Statement Analysis', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(df):
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Transaction Details", ln=True)
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Date", 1, 0, 'C', 1)
    pdf.cell(70, 10, "Description", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Amount", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Category", 1, 1, 'C', 1)

    # Table Body
    pdf.set_font("Arial", size=10)
    for _, row in df.iterrows():
        pdf.cell(40, 10, row["date"].strftime("%Y-%m-%d"), 1)
        pdf.cell(70, 10, str(row["description"])[:30], 1)
        pdf.cell(30, 10, f"{row['amount']:.2f}", 1, 0, 'R')
        pdf.cell(40, 10, str(row['category']), 1, 1)

    # Total
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(110, 10, "Total", 1, 0, 'R')
    pdf.cell(30, 10, f"{df['amount'].sum():.2f}", 1, 0, 'R')
    pdf.cell(40, 10, "", 1, 1)

    # Expense Chart
    expenses = df[df["category"] != "Income"]
    if not expenses.empty:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Expense Analysis", ln=True, align='C')

        summary = expenses.groupby("category")["amount"].sum().abs()

        plt.figure(figsize=(8, 5))
        summary.plot(kind='bar')
        plt.title("Spending by Category")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            plt.savefig(tmp.name, dpi=100)
            pdf.image(tmp.name, x=15, y=30, w=180)

        plt.close()
        os.remove(tmp.name)

    return pdf.output(dest='S').encode('latin-1')
