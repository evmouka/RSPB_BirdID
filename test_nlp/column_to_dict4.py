# extract_structure.py
import pandas as pd
import pprint

def extract_column_structure(excel_file):
    """
    Extract the column structure from an Excel file where:
    - Row 1 contains main categories
    - Row 2 contains subcategories
    """
    # Read the Excel file
    df = pd.read_excel(excel_file, header=[0, 1])
    
    # Get the column structure
    columns = {}
    
    # df.columns gives tuples of (main_category, subcategory)
    for main_cat, sub_cat in df.columns:
        if main_cat not in columns:
            columns[main_cat] = []
        columns[main_cat].append(sub_cat)
    
    # Save as Python code
    with open('column_structure4.py', 'w') as f:
        f.write("# Column structure extracted from Excel file\n\n")
        f.write("columns = {\n")
        for main_cat, sub_cats in columns.items():
            f.write(f"    '{main_cat}': [\n")
            for sub_cat in sub_cats:
                f.write(f"        '{sub_cat}',\n")
            f.write("    ],\n")
        f.write("}\n")
    
    # Save pretty printed version
    with open('column_structure4.txt', 'w') as f:
        f.write("Column Structure:\n")
        pprint.pprint(columns, stream=f, indent=2)
    
    return columns

if __name__ == "__main__":
    # Replace with your Excel file name
    excel_file = "bird_data.xlsx"
    
    try:
        structure = extract_column_structure(excel_file)
        print("\nColumn structure has been extracted and saved to:")
        print("- column_structure.py (as Python code)")
        print("- column_structure.txt (pretty printed)")
        print("\nStructure overview:")
        pprint.pprint(structure)
        
        # Also show count of subcategories
        print("\nNumber of subcategories in each main category:")
        for main_cat, sub_cats in structure.items():
            print(f"{main_cat}: {len(sub_cats)} subcategories")
            
    except FileNotFoundError:
        print(f"Error: Could not find file '{excel_file}'")
        print("Make sure the Excel file is in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")