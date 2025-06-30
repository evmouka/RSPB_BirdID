import pandas as pd
# Read Excel with multi-level headers
df = pd.read_excel("bird_data.xlsx", header=[0, 1])

# Convert first row to dictionary with hierarchical structure
row_dict = df.iloc[0].to_dict()

# Pretty print to see the structure clearly
import pprint
pprint.pprint(row_dict)