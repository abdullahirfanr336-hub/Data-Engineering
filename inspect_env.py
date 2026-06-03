import pdfplumber
import os

def quick_inspect(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found.")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"PDF Opened: {pdf_path}")
            print(f"Number of Pages: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                print(f"\n--- Page {i+1} ---")
                chars = page.chars
                rects = page.rects
                circles = page.objects.get('circle', [])
                curves = page.curves
                
                print(f"Chars: {len(chars)}")
                print(f"Rects: {len(rects)}")
                print(f"Circles: {len(circles)}")
                print(f"Curves: {len(curves)}")
                
                if chars:
                    print(f"Text Sample: {''.join([c['text'] for c in chars[:100]])}")
                
                # Look for header keywords to anchor columns
                words = page.extract_words()
                headers = [w for w in words if w['text'].lower() in ['referenz', 'style', 'fr', 'motor', 'leistung']]
                for h in headers:
                    print(f"Header: '{h['text']}' at x0={h['x0']}, x1={h['x1']}, top={h['top']}")

                # Inspect a few small objects
                small_rects = [r for r in rects if r['width'] < 15 and r['height'] < 15]
                if small_rects:
                    print(f"Found {len(small_rects)} small rects. Sample: {small_rects[0]}")
                
                small_circles = [c for c in circles if c['width'] < 15]
                if small_circles:
                    print(f"Found {len(small_circles)} small circles. Sample: {small_circles[0]}")

    except Exception as e:
        print(f"FAILED to read PDF: {e}")

if __name__ == "__main__":
    # Check multiple recent uploads
    uploads_dir = r"c:\Users\oes\Desktop\data engineering\uploads"
    dirs = [d for d in os.listdir(uploads_dir) if os.path.isdir(os.path.join(uploads_dir, d))]
    for d in dirs[-3:]: # Check last 3 uploads
        pdf_path = os.path.join(uploads_dir, d, "input.pdf")
        quick_inspect(pdf_path)
