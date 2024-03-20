from google.cloud import bigtable
from google.cloud.bigtable import row_filters
import ast

from main import is_literal

# Create a Bigtable client
client = bigtable.Client(project='wellsfargo-genai24-8021', admin=True)

# Get a reference to a Bigtable instance and table
instance = client.instance('hackathon2024')
table = instance.table('entity_metrics')

# Read the row for 'nordson' from the table
row = table.read_row('idex')

if row is not None:
    # Get the ESG types from the row
    esg_types = [esgType.decode('utf-8') for esgType in row.cells['cf1'].keys()]

    # Get the ESG indicators for each ESG type
    for esg_type in esg_types:
        cell = row.cells['cf1'][esg_type.encode('utf-8')][0]
        value = cell.value.decode('utf-8')
        esg_indicator = ast.literal_eval(value) if is_literal(value) else value

        # Ignore if the ESG type value is one of the specified ignored values
        ignored_values = ['Not provided', 'Not specified', 'null', 'none']
        if esg_type not in ignored_values and esg_indicator not in ignored_values:
            print(f'ESG Type: {esg_type}, ESG Indicators: {esg_indicator}')
else:
    print('Entity nordson not found')