import os
import scipy.stats
import pandas as pd
import yaml

# Load parameters from YAML file
with open("params.yaml", 'r') as file:
    params_data = yaml.safe_load(file)

# Extract year from parameters
year = params_data['year']

# Initialize lists to store DataFrame filenames
df_truth_filenames = []
df_predict_filenames = []

# Collect filenames from ground truth and predicted folders
for filename in os.listdir(f'groundtruth/{year}'):
    df_truth_filenames.append(filename)

for filename in os.listdir(f'predicted/{year}'):
    df_predict_filenames.append(filename)

# File path for fields list
fields_file_path = f'fieldlist/{year}/fields.txt'

# Read fields from the fields list file
fields = []
with open(fields_file_path, 'r') as file:
    for field in file:
        fields.append(field.strip())

# Create output folder for R-squared scores
out_folder = f'r2score/{year}'
os.makedirs(out_folder, exist_ok=True)

# Initialize list to store R-squared scores
r_squared_results = []

# File paths for ground truth and predicted data
truth_path = f'groundtruth/{year}'
predict_path = f'predicted/{year}'

# Iterate through each pair of ground truth and predicted files
for i in range(len(df_truth_filenames)):
    # Get the file paths for each pair
    truth_file_path = os.path.join(truth_path, df_truth_filenames[i])
    predict_file_path = os.path.join(predict_path, df_predict_filenames[i])

    # Read the ground truth and predicted data into DataFrames
    df_ground_truth = pd.read_csv(truth_file_path)
    df_predicted = pd.read_csv(predict_file_path)

    # Align predicted data length with ground truth data length
    df_predicted = df_predicted[:len(df_ground_truth)]

    # Align predicted columns with ground truth columns
    df_predicted['MonthlyMaximumTemperature'] = df_predicted['DailyMaximumDryBulbTemperature']
    df_predicted['MonthlyMinimumTemperature'] = df_predicted['DailyMinimumDryBulbTemperature']
    df_predicted = df_predicted.drop(columns=fields)

    # Calculate R-squared values for each temperature column
    _, _, r_squared_max_temp, _, _ = scipy.stats.mstats.linregress(
        df_ground_truth['MonthlyMaximumTemperature'],
        df_predicted['MonthlyMaximumTemperature']
    )
    _, _, r_squared_min_temp, _, _ = scipy.stats.mstats.linregress(
        df_ground_truth['MonthlyMinimumTemperature'],
        df_predicted['MonthlyMinimumTemperature']
    )

    # Store R-squared values in a dictionary
    r_squared_values = {
        'MonthlyMaximumTemperature': r_squared_max_temp ** 2,
        'MonthlyMinimumTemperature': r_squared_min_temp ** 2
    }

    # Append R-squared values to the results list
    r_squared_results.append({df_truth_filenames[i]: r_squared_values})

# Write R-squared results to a text file
result_file_path = os.path.join(out_folder, 'res.txt')
with open(result_file_path, 'w') as file:
    for item in r_squared_results:
        file.write("%s\n" % item)




