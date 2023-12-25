
import pandas as pd
import seaborn as sns
from os.path import exists
import matplotlib.pyplot as plt

# Verify if seaborn is already installed, otherwise install it
try:
    import seaborn
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'seaborn'])

# The Titanic dataset local file path
file_path = 'titanic.csv'

# Check if the Titanic dataset csv file exists
if not exists(file_path):
    print(f'File not found: {file_path}')
    # Download the Titanic dataset if it doesn't exist
    import requests
    TITANIC_DATASET_URL = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
    response = requests.get(TITANIC_DATASET_URL)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print('Titanic dataset downloaded successfully.')

# Load the dataset into a pandas DataFrame
try:
    data = pd.read_csv(file_path)
    print('Dataset loaded successfully.')
except Exception as e:
    print(f'Error loading the dataset: {e}')
    raise

# Prepare the data: clean it and calculate survival rates by age
try:
    # Drop NaN ages
    data = data.dropna(subset=['Age'])
    # Calculate survival rates by age
    survival_rates = data.groupby('Age')['Survived'].mean()
    print('Survival rates by age calculated successfully.')
except Exception as e:
    print(f'Error calculating survival rates: {e}')
    raise

# Plot the survival rates by age as a histogram
try:
    plt.figure(figsize=(12, 7))
    sns.barplot(x=survival_rates.index, y=survival_rates.values)
    plt.title('Titanic Survival Rates by Age')
    plt.xlabel('Age')
    plt.ylabel('Survival Rate')
    plt.show()
    print('Histogram plotted successfully.')
except Exception as e:
    print(f'Error plotting the histogram: {e}')
    raise
