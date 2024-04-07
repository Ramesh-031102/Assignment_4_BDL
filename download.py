import requests
import os
from bs4 import BeautifulSoup
import yaml

# Load parameters from YAML file
with open("params.yaml", 'r') as f:
    params_data = yaml.safe_load(f)
    print(params_data)

# Function to download files based on the specified year and number of locations
def download_files(year, num_locations):
    # Construct the base URL and download folder path
    base_url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'
    download_folder = f'downloaded_files/{year}'

    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Send a GET request to the base URL
    response = requests.get(base_url)
    if response.status_code == 200:  # Check if the request was successful
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')  # Find the table containing the files
        if table:
            anchors = table.find_all('a')  # Find all <a> tags within the table
            anchors.reverse()  # Reverse the list of anchors

            num_files_downloaded = 0  # Initialize the counter for downloaded files

            for anchor in anchors:
                if num_files_downloaded >= num_locations:
                    break  # Stop if the desired number of files has been downloaded

                file_name = anchor.text
                if file_name.endswith('.csv'):  # Download only CSV files
                    file_url = f'{base_url}/{file_name}'  # Construct the file URL
                    try:
                        # Send a GET request to download the file
                        request_file = requests.get(file_url)
                        if request_file.status_code == 200:  # Check if the download was successful
                            # Write the downloaded content to a file in the download folder
                            with open(os.path.join(download_folder, file_name), 'wb') as file:
                                file.write(request_file.content)
                            num_files_downloaded += 1  # Increment the downloaded file counter
                            print(f'Downloaded: {file_name}')  # Print a success message
                        else:
                            print(f'Download failed: {file_url}')  # Print a failure message
                    except Exception as error:
                        print(f"Error while downloading : {file_url}. Error: {error}")  # Print any download errors
        else:
            print('Table not found in page')  # Print a message if the table is not found
    else:
        print(f'Failed to retrieve data in {year}')  # Print a message if the request fails

# Call the download_files function with parameters from the YAML file
download_files(params_data['year'], params_data['nlocs'])























