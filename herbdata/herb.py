import pandas as pd
import json

# Read data from the Excel file
excel_data = pd.read_excel('FreshHerbsWithPicture_url.xlsx')

# Convert the data to JSON
json_data = excel_data.to_json(orient='records')

# Write the JSON data to a file
with open('dataset_7.json', 'w') as file:
    file.write(json_data)
