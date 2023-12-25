# Import necessary libraries



import pandas as pd


def load_data(file_path):
    """
    Load the Titanic dataset from a specified CSV file path into a pandas DataFrame.

    :param file_path: str, represents the path to the CSV file containing the dataset
    :return: pandas DataFrame containing the loaded dataset
    """
    # Read the CSV file using pandas and return the DataFrame
    return pd.read_csv(file_path)


import seaborn as sns
import matplotlib.pyplot as plt

def visualize_passenger_class_distribution(dataframe, column='Pclass'):
    """
    Visualize the distribution of passenger classes in a dataset using a seaborn countplot.

    Parameters:
    dataframe (pandas.DataFrame): The data frame containing the passenger class information.
    column (str): The column name in the dataframe that contains the passenger class data.

    Returns:
    None: The function will display a countplot and does not return anything.

    """
    # Check if the column exists in the dataframe
    if column not in dataframe.columns:
        raise ValueError(f'Column {column} does not exist in the dataframe.')

    # Create a seaborn countplot to visualize the distribution of passenger classes
    plt.figure(figsize=(10, 6))
    sns.countplot(data=dataframe, x=column, palette='coolwarm')
    plt.title('Passenger Class Distribution')
    plt.xlabel('Passenger Class')
    plt.ylabel('Number of Passengers')
    plt.show()



import pandas as pd
import matplotlib.pyplot as plt

def visualize_survival_rates(df, title='Survival Rates by Class and Gender'):
    """
    Visualize survival rates by passenger class and gender using a bar chart.

    Parameters:
    df (DataFrame): A pandas DataFrame containing the dataset with variables 'Pclass', 'Sex', and 'Survived'.
    title (str): Title for the plot (default is 'Survival Rates by Class and Gender').

    Returns:
    None: The function will display a bar plot and returns None.
    """
    survival_rates = df.groupby(['Pclass', 'Sex'])['Survived'].mean().unstack()
    survival_rates.plot(kind='bar')

    plt.title(title)
    plt.xlabel('Passenger Class')
    plt.ylabel('Survival Rate')
    plt.xticks(rotation=0)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.show()

# Example of how to use the function, assuming you have a dataset `titanic_df`:
# visualize_survival_rates(titanic_df)



import matplotlib.pyplot as plt
import seaborn as sns

def visualize_age_distribution(data):
    """
    Function to visualize the age distribution of passengers.
    
    Parameters:
        data (pandas.DataFrame): A dataframe containing at least an 'Age' column.
    
    Returns:
        The function doesn't return anything. It shows a histogram plot.
    
    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'Age': [22, 34, 18, 29, 45, 58, 7]})
        >>> visualize_age_distribution(df)
    """
    # Check if 'Age' column exists in the dataframe
    if 'Age' not in data.columns:
        raise ValueError("The DataFrame doesn't contain an `Age` column.")

    # Create the histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Age', bins=30, kde=True)
    plt.title('Age Distribution of Passengers')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()
