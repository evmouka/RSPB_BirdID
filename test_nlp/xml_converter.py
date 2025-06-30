import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def bird_excel_to_xml(excel_file, output_file):
    """
    Convert hierarchical bird Excel data to XML.
    """
    # Define your column structure
    columns = {
    'Key Species Information': [
        'Species number',
        'Name',
        'Latin name',
        'Alt names/ mispellings',
        'Sex/ Age Variations',
        'Seasonal Variations',
        'Conservation status',
        'Group',
        'Time of year active (UK)',
        'Summary (200 characters)',
    ],
    'Media': [
        'Picture (Primary)',
        'Picture 2',
        'Picture 3',
        'Picture 4',
        'Illustration',
        'Audio',
        'Distribution map',
    ],
    'Key features': [
        'Plumage colour(s)',
        'Beak Colour(s)',
        'Feet colour(s)',
        'Leg colour(s)',
        'Beak Shape 1',
        'Beak shape 2 (optional)',
        'Tail shape 1',
        'Tail shape 2 (optional)',
        'Pattern/ Markings',
        'Diet',
        'Population (UK)',
        'Min Length (cm)',
        'Max Length (cm)',
        'Mean length (cm)',
        'Size',
        'Wingspan (cm)',
        'Weight (g)',
        'Habitat(s)',
    ],
    'How to identify': [
        'Appearance',
        'Size',
        'Habitat',
        'Call',
        'Behaviour',
    ],
    'Trivia': [
        'Fact 1',
        'Fact 2',
        'Fact 3',
    ],
    'Other': [
        'Similar species',
        'Where to see them (countries)',
    ],
}
    # Read Excel file with multi-level columns
    df = pd.read_excel(excel_file, header=[0, 1])
    
    # Create root element
    root = ET.Element("birds")
    
    # Convert each row to XML
    for idx, row in df.iterrows():
        bird = ET.SubElement(root, "bird")
        
        # Process each main column and its subcolumns
        for main_col, subcols in columns.items():
            section = ET.SubElement(bird, main_col.lower().replace(' ', '_'))
            
            for subcol in subcols:
                try:
                    value = row[(main_col, subcol)]
                    if pd.notna(value):  # Check if value is not NA/empty
                        elem = ET.SubElement(section, subcol.lower().replace(' ', '_'))
                        
                        # Handle comma-separated values
                        if isinstance(value, str) and ',' in value:
                            for item in value.split(','):
                                item_elem = ET.SubElement(elem, 'value')
                                item_elem.text = item.strip()
                        else:
                            elem.text = str(value)
                except KeyError:
                    continue  # Skip if column doesn't exist
    
    # Create the XML string with proper formatting
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

# Example usage
if __name__ == "__main__":
    # Define your file paths
    input_file = "bird_data.xlsx"  # Change this to your Excel file name
    output_file = "bird_data.xml"  # Change this to your desired output file name
    
    bird_excel_to_xml(input_file, output_file)