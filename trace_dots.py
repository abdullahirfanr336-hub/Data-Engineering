import pdfplumber
import os

def trace_dots(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()
        
        # 1. Identify Column Anchors
        # We need to find the X positions of the models (Reference, Style, FR)
        anchors = {}
        for w in words:
            txt = w['text'].lower()
            if 'referenz' in txt: anchors['Referenz'] = w['x0']
            if 'style' in txt: anchors['Style'] = w['x0']
            if 'fr' == txt: anchors['FR'] = w['x0']

        print(f"DEBUG: Anchors found: {anchors}")

        # 2. Extract Dots (Small shapes)
        dots = []
        for obj_type in ['rect', 'circle', 'curve']:
            for obj in page.objects.get(obj_type, []):
                if obj['width'] < 15 and obj['height'] < 15:
                    dots.append({'type': obj_type, 'x0': obj['x0'], 'top': obj['top']})

        print(f"DEBUG: Total Dots detected: {len(dots)}")

        # 3. Associate Dots with Rows
        text_lines = page.extract_text_lines()
        for i, line in enumerate(text_lines[:20]): # First 20 lines
            txt = line['text'].strip()
            y_range = (line['top'] - 2, line['bottom'] + 2)
            
            row_dots = []
            for d in dots:
                if y_range[0] <= d['top'] <= y_range[1]:
                    row_dots.append(d)
            
            if row_dots:
                print(f"Row {i}: '{txt}'")
                for rd in row_dots:
                    print(f"   Dot at x0={rd['x0']} (Type: {rd['type']})")

if __name__ == "__main__":
    target_pdf = r"c:\Users\oes\Desktop\data engineering\uploads\fd6dc235-f7eb-4a55-a9d6-9b1287c56c9c\input.pdf"
    trace_dots(target_pdf)
