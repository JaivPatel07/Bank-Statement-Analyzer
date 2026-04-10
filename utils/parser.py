import pandas as pd
from utils.ai_engine import get_ai_categories

def normalize_columns(df):
    mapping = {
        'date': ['date', 'transaction date', 'txn date', 'value date'],
        'description': ['description', 'particulars', 'narration', 'transaction details', 'details'],
        'amount': ['amount', 'transaction amount', 'withdrawal/deposit', 'debit/credit', 'balance']
    }
    
    new_cols = {}
    for standard, variations in mapping.items():
        for col in df.columns:
            if col.lower().strip() in variations:
                new_cols[col] = standard
                break
    
    return df.rename(columns=new_cols)

def categorize(description: str) -> str:
    d = str(description).lower()
    if "uber" in d or "ola" in d or "taxi" in d or "train" in d or "flight" in d:
        return "Transport"
    elif "restaurant" in d or "cafe" in d or "coffee" in d or "zomato" in d or "swiggy" in d:
        return "Food"
    elif "salary" in d or "freelance" in d:
        return "Income"
    elif "electricity" in d or "water" in d or "internet" in d or "bill" in d:
        return "Bills"
    elif "grocery" in d or "store" in d or "mart" in d:
        return "Groceries"
    elif "amazon" in d or "flipkart" in d or "shopping" in d:
        return "Shopping"
    else:
        return "Others"

def parse_csv(file, use_ai=False) -> pd.DataFrame:
    try:
        df = pd.read_csv(file)
        df = normalize_columns(df)
        
        required = ['date', 'description', 'amount']
        if not all(col in df.columns for col in required):
            return None
            
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'amount'])
        
        if use_ai:
            unique_desc = df['description'].unique().tolist()
            ai_cats = get_ai_categories(unique_desc)
            if ai_cats:
                df['category'] = df['description'].map(ai_cats).fillna("Others")
            else:
                df['category'] = df['description'].apply(categorize)
        else:
            df['category'] = df['description'].apply(categorize)
            
        return df
    except Exception as e:
        print(f"Parsing error: {e}")
        return None
