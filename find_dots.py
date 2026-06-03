import pdfplumber
import os

def exhaustive_inspect(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        # 1. Inspect all unique characters and their counts
        print("--- Character Inventory ---")
        char_counts = {}
        for char in page.chars:
            txt = char['text']
            char_counts[txt] = char_counts.get(txt, 0) + 1
        
        # Sort by frequency
        sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
        for char, count in sorted_chars:
            if ord(char[0]) > 127 or count < 100: # Show suspicious ones
                 print(f"Char: '{char}' | Count: {count} | Hex: {[hex(ord(c)) for c in char]}")

        # 2. Check for small geometric objects of any type
        print("\n--- Geometric Object Analysis ---")
        for obj_type, objs in page.objects.items():
            small_ones = [o for o in objs if o.get('width', 99) < 20 or o.get('height', 99) < 20]
            print(f"{obj_type}: {len(objs)} total, {len(small_ones)} small (<20px)")
            if small_ones:
                print(f"  Sample Small {obj_type}: {small_ones[0]}")

        # 3. Try to extract a table and see what's in the 'dot' columns
        print("\n--- Raw Table Row Snippet ---")
        table = page.extract_table()
        if table:
            for row in table[:10]: # First 10 rows
                 print(f"  Row: {row}")

if __name__ == "__main__":
    target_pdf = r"c:\Users\oes\Desktop\data engineering\uploads\fd6dc235-f7eb-4a55-a9d6-9b1287c56c9c\input.pdf"
    exhaustive_inspect(target_pdf)
