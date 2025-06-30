import pandas as pd
import pprint

def get_column_structure(excel_file, row_number=0):
    """
    Read an Excel file and convert a specific row to a dictionary.
    Handles multi-level headers.
    
    Parameters:
    excel_file (str): Path to Excel file
    row_number (int): Which row to convert (default is first row)
    """
    # Read Excel with multi-level headers
    df = pd.read_excel(excel_file, header=[0, 1])
    
    # Convert specified row to dictionary
    row_dict = df.iloc[row_number].to_dict()
    
    # Save pretty printed version
    with open('column_structure.txt', 'w') as f:
        f.write("Column Structure:\n")
        pprint.pprint(row_dict, stream=f, indent=2)
    
    # Save as Python script format
    with open('row1.txt', 'w') as f:
        f.write("row_dict = {\n")
        for key, value in row_dict.items():
            # Format the tuple key and handle different value types
            if isinstance(value, str):
                f.write(f"    {key}: '{value}',\n")
            elif pd.isna(value):
                f.write(f"    {key}: None,\n")
            else:
                f.write(f"    {key}: {value},\n")
        f.write("}\n")
    
    return row_dict

if __name__ == "__main__":
    # Replace with your Excel file name
    excel_file = "bird_data.xlsx"
    
    try:
        # Get and display the structure
        structure = get_column_structure(excel_file)
        print("\nColumn structure has been saved to 'column_structure.txt'")
        print("Python dictionary format has been saved to 'row1.txt'")
        print("\nDictionary structure:")
        pprint.pprint(structure, indent=2)
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{excel_file}'")
        print("Make sure the Excel file is in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")