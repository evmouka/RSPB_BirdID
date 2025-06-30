import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def clean_xml_name(text):
    """Clean text for use as XML element names"""
    if pd.isna(text):
        return "empty"
    # Remove special characters and replace spaces/slashes with underscores
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    clean = clean.replace(' ', '_').replace('/', '_')
    # Remove leading digits if any
    clean = re.sub(r'^\d+', '', clean)
    # If empty after cleaning, return a default
    return clean if clean else "item"

def clean_xml_value(value):
    """Clean text for use as XML values"""
    if pd.isna(value):
        return ""
    return str(value).strip()

def bird_excel_to_xml(excel_file, output_file):
    """
    Convert hierarchical bird Excel data to XML.
    """
    # Your existing columns dictionary remains the same
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
    
    # Read Excel file
    df = pd.read_excel(excel_file, header=[0, 1])
    
    # Create root element
    root = ET.Element("birds")
    
    # Convert each row to XML
    for idx, row in df.iterrows():
        bird = ET.SubElement(root, "bird")
        bird.set('id', str(idx + 1))
        
        # Process each main column and its subcolumns
        for main_col, subcols in columns.items():
            # Clean main column name for XML
            main_elem_name = clean_xml_name(main_col)
            section = ET.SubElement(bird, main_elem_name)
            
            for subcol in subcols:
                try:
                    value = row.get((main_col, subcol))
                    if pd.notna(value):
                        # Clean subcol name for XML
                        sub_elem_name = clean_xml_name(subcol)
                        elem = ET.SubElement(section, sub_elem_name)
                        
                        # Handle comma-separated values
                        if isinstance(value, str) and ',' in value:
                            values = [v.strip() for v in value.split(',')]
                            for item in values:
                                if item:  # Only add non-empty values
                                    item_elem = ET.SubElement(elem, 'value')
                                    item_elem.text = clean_xml_value(item)
                        else:
                            elem.text = clean_xml_value(value)
                except (KeyError, TypeError):
                    continue
    
    try:
        # Convert to string with proper encoding
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        # Pretty print
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="    ")
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
            
    except Exception as e:
        print(f"Error in XML processing: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        input_file = "bird_data.xlsx"
        output_file = "bird_data.xml"
        bird_excel_to_xml(input_file, output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")