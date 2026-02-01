import pandas as pd

def categorize(description):
    d = str(description).lower()
    if "uber" in d or "ola" in d:
        return "Transport"
    elif "restaurant" in d or "cafe" in d:
        return "Food"
    elif "salary" in d:
        return "Income"
    elif "electricity" in d:
        return "Bills"
    elif "grocery" in d:
        return "Groceries"
    else:
        return "Other"

def parse_csv(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    return df
