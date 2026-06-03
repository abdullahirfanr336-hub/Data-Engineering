import pdfplumber
import pandas as pd
import os

class PDFExtractor:
    """
    Handles PDF extraction, including tables and visual markers (dots).
    """
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_features(self):
        """
        Extracts equipment features and their availability (dots) across models.
        """
        data = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # 1. Find the table area. We'll look for horizontal lines or text columns.
                # In these SEAT PDFs, dots are usually circles or rectangles at specific X positions.
                
                # 1. Identify dots (Character based in this PDF)
                # We found (cid:127) is the dot character
                dots = [c for c in page.chars if '(cid:127)' in c['text'] or ord(c['text'][0]) == 127]
                
                # Also fallback to small rects/circles if cid:127 isn't found
                if not dots:
                    circles = page.objects.get("circle", [])
                    rects = page.objects.get("rect", [])
                    dots = [c for c in circles if c['width'] < 12]
                    dots += [r for r in rects if r['width'] < 12]

                print(f"DEBUG: Page {page.page_number} - Found {len(dots)} dots")

                # 2. Dynamically find column headers for dots
                dynamic_cols = {}
                words = page.extract_words()
                for obj in words:
                    text = obj['text'].lower()
                    if 'referenz' in text:
                        dynamic_cols['Referenz'] = (obj['x0'] - 30, obj['x1'] + 30)
                    elif 'style' in text:
                        dynamic_cols['Style'] = (obj['x0'] - 30, obj['x1'] + 30)
                    elif 'fr' == text or ('fr' in text and len(text) < 5):
                        dynamic_cols['FR'] = (obj['x0'] - 30, obj['x1'] + 30)

                print(f"DEBUG: Columns detected: {dynamic_cols}")

                # 3. Associate text features with dots
                text_instances = page.extract_text_lines()
                current_category = "General"
                
                # Pre-bin dots by Y-coordinate for faster lookup
                # We'll use a tolerance of 5px for the Y-range
                dot_y_map = {}
                for d in dots:
                    y_key = int(d['top'] // 5)
                    if y_key not in dot_y_map: dot_y_map[y_key] = []
                    dot_y_map[y_key].append(d)

                for line in text_instances:
                    feature_text = line['text'].strip()
                    if not feature_text or len(feature_text) < 3: continue
                    
                    y_top = line['top']
                    y_bottom = line['bottom']

                    # Category detection
                    potential_cats = ['Sicherheits-', 'Innere', 'Außenbereich', 'Infotainment', 'Räder & Reifen', 'Pakete', 'Technik']
                    if any(c in feature_text for c in potential_cats) and line['x0'] < 100:
                        current_category = feature_text
                        continue

                    # Map dots to this row using the optimized Y-map
                    row_data = {"feature": feature_text, "type": current_category}
                    
                    # Fetch relevant dots (in current Y bucket and adjacent ones)
                    y_keys = [int(y_top // 5), int(y_bottom // 5)]
                    # Unique keys
                    y_keys = list(set(y_keys))
                    relevant_dots = []
                    for k in y_keys:
                        relevant_dots.extend(dot_y_map.get(k, []))
                    
                    for col_name, (x_min, x_max) in dynamic_cols.items():
                        has_dot = any(x_min <= d['x0'] <= x_max and (y_top - 4) <= d['top'] <= (y_bottom + 4) for d in relevant_dots)
                        row_data[col_name] = 1 if has_dot else ""
                    
                    if len(row_data) > 2:
                        data.append(row_data)
        
        return data

if __name__ == "__main__":
    # Testing logic will go here
    print("PDFExtractor initialized.")
