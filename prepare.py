import pandas as pd
import os
import yaml

# Load parameters from YAML file
with open("params.yaml", 'r') as file:
    params_data = yaml.safe_load(file)

# Define input and output folders
input_folder = 'downloaded_files/2003'
output_folder = 'groundtruth/2003'
os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

# Extract year from parameters
year = params_data['year']

# Define columns for monthly and daily data
monthly_columns = ['MonthlyMaximumTemperature', 'MonthlyMinimumTemperature']
daily_columns = ['DailyMaximumDryBulbTemperature', 'DailyMinimumDryBulbTemperature']

# Create field list folder for the year if it doesn't exist
field_list_folder = f'fieldlist/{year}'
os.makedirs(field_list_folder, exist_ok=True)

# Loop through files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # Process CSV files only
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)  # Read CSV file into a DataFrame
        df_dropped = df.dropna(subset=monthly_columns, axis=0)  # Drop rows with missing monthly data
        df_dropped['MONTH'] = pd.to_datetime(df_dropped['DATE']).dt.month  # Extract month from date
        df_dropped = df_dropped[['MONTH'] + monthly_columns]  # Keep only required columns
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_dropped.csv')
        df_dropped.to_csv(output_file_path, index=False)  # Save processed data to output folder

# Write daily_columns to a file in the field list folder
with open(os.path.join(field_list_folder, 'fields.txt'), 'w') as file:
    for item in daily_columns:
        file.write("%s\n" % item)

