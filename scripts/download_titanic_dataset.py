
import requests
from pathlib import Path

# URL of the Titanic dataset CSV file
TITANIC_DATASET_URL = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'

# Local path to save the Titanic dataset
LOCAL_DATASET_PATH = Path('titanic.csv')

if not LOCAL_DATASET_PATH.exists():
    # Download the Titanic dataset
    response = requests.get(TITANIC_DATASET_URL)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    
    # Write the content of the response to a local file
    with open(LOCAL_DATASET_PATH, 'wb') as file:
        file.write(response.content)
else:
    print(f'Dataset already exists at: {LOCAL_DATASET_PATH}')

# Run verification of file existence
print(f'Download verification: {LOCAL_DATASET_PATH.exists()}')
