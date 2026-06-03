import pandas as pd

class DataTransformer:
    """
    Cleans and transforms extracted PDF data for Excel export.
    """
    HEADER_MAPPING = {
        'Referenz': 'reference_col', # Use a unique name first
        'Style': 'style',
        'FR': 'fr',
        'Motor': 'motor',
        'Leistung (kW/PS)': 'power',
        'Getriebe': 'transmission',
        'Code': 'code',
        'Listenpreis1': 'price'
    }

    CATEGORY_MAPPING = {
        'Sicherheits- und Assistenzsysteme': 'Safety',
        'Innere': 'Interior',
        'Außenbereich': 'Exterior',
        'Infotainment': 'Infotainment',
        'Räder & Reifen': 'Wheels'
    }

    def __init__(self):
        pass

    def transform(self, df):
        """
        Applies cleaning rules:
        1. Deduplicates columns.
        2. Translates headers.
        3. Normalizes boolean values (dots -> 1/0 or Yes/No).
        4. Implements Keyword Mapping Logic (FR rule).
        """
        # 0. Deduplicate columns
        df = df.loc[:, ~df.columns.duplicated()].copy()

        # 1. Rename columns
        df = df.rename(columns=self.HEADER_MAPPING)

        # 2. Keyword Mapping Logic (CRITICAL RULE #3)
        if 'feature' in df.columns and 'type' in df.columns:
            feature_col = df['feature'].astype(str)
            mask = feature_col.str.contains('Multifunktionslenkrad|Multifunction Steering Wheel', case=False, na=False)
            df.loc[mask, 'type'] = 'Innere'

        # 3. Add Metadata Columns per Image 4
        # columns: online, details, code, export_ext, attribute, FILTERABL, Style, cat, S
        df['online'] = 1
        df['details'] = 1
        df['code'] = 1
        df['export_ext'] = 1
        df['attribute'] = 1
        df['FILTERABL'] = 1
        df['Style'] = 1
        df['cat'] = 1
        df['S'] = 1

        # 4. Format 'type' to match Image 4 (e.g., _Sicherhei, _Innen)
        type_mapping = {
            'Safety': '_Sicherhei',
            'Interior': '_Innen',
            'Exterior': '_Außen',
            'Infotainment': '_Infotainm',
            'Wheels': '_Räder & '
        }
        if 'type' in df.columns:
            df['type'] = df['type'].map(type_mapping).fillna(df['type'])

        # 5. Finally rename 'feature' to 'name'
        df = df.rename(columns={'feature': 'name'})

        return df

    def finalize_types(self, df):
        """Translates category types to the clean strings expected."""
        if 'type' in df.columns:
            df['type'] = df['type'].map(self.CATEGORY_MAPPING).fillna(df['type'])
        return df

if __name__ == "__main__":
    print("DataTransformer initialized.")
