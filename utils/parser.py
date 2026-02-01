import pandas as pd

def categorize(description: str) -> str:
    """
    Categorizes a transaction based on its description.

    Args:
        description (str): The transaction description.

    Returns:
        str: The category of the transaction (e.g., 'Transport', 'Food').
    """
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

def parse_csv(file) -> pd.DataFrame:
    """
    Parses a CSV file into a pandas DataFrame with normalized column names.

    Args:
        file: The path to the CSV file or a file-like object.

    Returns:
        pd.DataFrame: The parsed DataFrame with lowercase column names.
    """
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    return df
