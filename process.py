import pandas as pd
import numpy as np
import os
import yaml

# Load parameters from YAML file
with open("params.yaml", 'r') as file:
    params_data = yaml.safe_load(file)

# Extract year from parameters
year = params_data['year']

# Define input and output folders
input_folder = f"downloaded_files/{year}"
output_folder = f'predicted/{year}'
os.makedirs(output_folder, exist_ok=True)

# File path for fields list
fields_file_path = f'fieldlist/{year}/fields.txt'

# Read fields from the fields list file
fields = []
with open(fields_file_path, 'r') as file:
    for field in file:
        fields.append(field.strip())

# Process each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)  # Read CSV file into DataFrame

        # Drop rows with missing data in specified fields
        df_dropped = df.dropna(subset=fields, axis=0)
        df_dropped['MONTH'] = pd.to_datetime(df_dropped['DATE']).dt.month  # Extract month from date

        # Remove non-numeric characters from selected fields
        for field in fields:
            df_dropped[field] = df_dropped[field].astype(str).str.replace('[a-zA-Z]', '', regex=True)

        # Replace empty strings with NaN and drop rows with missing data in selected fields
        df_dropped.replace({'': np.nan}, inplace=True)
        df_dropped = df_dropped.dropna(subset=fields, axis=0)

        # Convert selected fields to float data type
        for field in fields:
            df_dropped[field] = df_dropped[field].astype(float)

        # Calculate monthly averages for selected fields
        monthly_averages = {}
        for field in fields:
            monthly_averages[field] = df_dropped.groupby('MONTH', as_index=False)[field].mean()

        # Concatenate monthly averages into a single DataFrame
        concat_list = [monthly_averages[field].set_index('MONTH') for field in fields]
        concat_df = pd.concat(concat_list, axis=1)

        # Save processed data to output file
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_filtered.csv')
        concat_df.to_csv(output_file_path, index=True)

