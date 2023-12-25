import os

# Define the path to the scripts directory
scripts_dir = 'scripts'

# Function to read and print the content of a file
def read_file(file_path):
    """Read the content of a file and print it.

    :param file_path: str
        The path to the file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except Exception as e:
        print(f'An error occurred while reading the file: {e}')

# Path to 'water_simulation_with_borders.py' within the scripts directory
file_path = os.path.join(scripts_dir, 'water_simulation_with_borders.py')

# Main execution
def main():
    # Invoke the read_file function with the correct file path
    read_file(file_path)

if __name__ == '__main__':
    main()