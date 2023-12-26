import os

# Define the path to the script file
script_path = './scripts/dice_physics_refinement.py'

# Function to read the content of the script
def read_script_content(path):
    """Read the content of the given script file.

    Args:
        path (str): The path to the script file.

    Returns:
        str: The content of the script file.
    """
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
        return content
    else:
        return 'File not found.'

# Main function
def main():
    content = read_script_content(script_path)
    print(content)

# Execute the main function
if __name__ == '__main__':
    main()
