import os
import sys
from parser import PDFExtractor
from transformer import DataTransformer
from writer import ExcelWriter

def run_pipeline(input_pdf, output_xlsx):
    if not os.path.exists(input_pdf):
        print(f"Error: PDF not found at {input_pdf}")
        return

    print(f"Starting pipeline for {input_pdf}...")

    # 1. Extraction
    extractor = PDFExtractor(input_pdf)
    raw_data = extractor.extract_features()
    
    # Convert to DataFrame for easier handling
    import pandas as pd
    df = pd.DataFrame(raw_data)

    # 2. Transformation
    transformer = DataTransformer()
    clean_df = transformer.transform(df)
    clean_df = transformer.finalize_types(clean_df)

    # 3. Writing
    writer = ExcelWriter(output_xlsx)
    writer.save(clean_df)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    # Example usage
    # pdf_file = "sample_seat_ibiza.pdf"
    # output_file = "output_data.xlsx"
    # run_pipeline(pdf_file, output_file)
    print("Main script ready. Use run_pipeline(input, output) to start.")
