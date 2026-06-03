import os
import pandas as pd
from main import run_pipeline

def verify_final():
    pdf_path = r"c:\Users\oes\Desktop\data engineering\uploads\fd6dc235-f7eb-4a55-a9d6-9b1287c56c9c\input.pdf"
    excel_path = "final_verification.xlsx"
    
    # Remove old verify file if exists
    if os.path.exists(excel_path):
        os.remove(excel_path)
    
    print(f"Running pipeline on {pdf_path}...")
    run_pipeline(pdf_path, excel_path)
    
    if os.path.exists(excel_path):
        print("Excel file generated successfully.")
        df = pd.read_excel(excel_path)
        print(f"Rows extracted: {len(df)}")
        print("\nColumn snippet (first 5 rows):")
        print(df.head())
        
        # Check for dots (values of 1)
        dot_count = (df == 1).sum().sum()
        print(f"\nTotal 'Dots' (1s) extracted: {dot_count}")
        
        if len(df) > 0 and dot_count > 0:
            print("\nSUCCESS: Extraction is WORKING.")
        else:
            print("\nFAILURE: Extraction returned empty or no dots.")
    else:
        print("FAILED: Excel file not generated.")

if __name__ == "__main__":
    verify_final()
