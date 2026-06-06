import pandas as pd
from pathlib import Path

# Paths
xlsx_path = Path(r"c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube bots automation\PsychologyScrolls\psychologyscrolls (1).xlsx")
txt_path = Path(r"c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube bots automation\PsychologyScrolls\psychologyscrolls.txt")

try:
    df = pd.read_excel(xlsx_path)
    print("Columns:", df.columns.tolist())
    print("First 5 rows:\n", df.head())
    
    # Assuming the quotes are in the first column or named 'Quote'
    quote_col = df.columns[0]
    if 'Quote' in df.columns:
        quote_col = 'Quote'
    elif 'Quotes' in df.columns:
        quote_col = 'Quotes'
        
    quotes = df[quote_col].dropna().astype(str).tolist()
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        for quote in quotes:
            f.write(quote.strip() + '\n')
            
    print(f"Successfully converted {len(quotes)} quotes to {txt_path}")
except Exception as e:
    print(f"Error: {e}")
