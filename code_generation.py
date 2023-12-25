import json
import re

import openai

from config import (
    OPENAI_API_KEY,
    OPENAI_CODE_MODEL,
    CODE_SYSTEM_PROMPT,
    TEMPLATE_SYSTEM_PROMPT
)

openai.api_key = OPENAI_API_KEY

def call_llm(prompt, context=""):
    """
    Calls the LLM with a given prompt and context.
    
    Parameters:
    prompt (str): The prompt to send to the LLM.
    context (str): Any additional context needed for the LLM to generate the response.
    
    Returns:
    str: The response from the LLM.
    """
    try:
        with openai.OpenAI(api_key = openai.api_key) as f:
            response = f.chat.completions.create(
                model=OPENAI_CODE_MODEL,
                messages=[
                        {"role": "system", "content": CODE_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                response_format={"type": "json_object"},
                timeout = 15
            )
        result = json.loads(response.choices[0].message.content)["python_code"]

    except Exception as e:
        print(e)
        result = "Coding unavailable currently, try again."
        
    return result

def generate_code_template(function_descriptions):
    """
    Generates a code template with blank functions and detailed docstrings.
    
    Parameters:
    function_descriptions (dict): A dictionary where keys are function names and values are descriptions.
    
    Returns:
    str: A string containing the Python code for the function templates.
    """
    prompt = TEMPLATE_SYSTEM_PROMPT
    for name, desc in function_descriptions.items():
        prompt += f"- Function name: {name}, Description: {desc}\n"
    
    return call_llm(prompt)

def implement_function(function_name, description, existing_code):
    """
    Implements a single function in the existing codebase.
    
    Parameters:
    function_name (str): The name of the function to implement.
    description (str): The description of the function to implement.
    existing_code (str): The existing code where the function implementation should be added.
    
    Returns:
    str: The updated code with the function implemented.
    """
    prompt = f"Give me the code for the function '{function_name}' in Python. Using this full context:\n\n{existing_code}"
    function_code = call_llm(prompt)
    
    return update_function_in_code(existing_code, function_name, function_code)

def update_function_in_code(existing_code, function_name, new_function_code):
    """
    Updates the implementation of a specific function in the existing code.

    Parameters:
    existing_code (str): The existing code as a string.
    function_name (str): The name of the function to update.
    new_function_code (str): The new code for the function.

    Returns:
    str: Updated code with the specified function replaced.
    """
    import re
    
    # Pattern to find the function definition
    pattern = f"(def {re.escape(function_name)}\s*\([^\)]*\):[\s\S]*?)(?=\n\s*\n|\Z)"

    # Finding matches
    matches = re.findall(pattern, existing_code)
    
    if matches:
        # Replace the entire function definition with the new code
        updated_code = re.sub(pattern, new_function_code, existing_code, count=1)
        return updated_code
    else:
        # Append if function not found, ensuring proper newline separation
        return existing_code.rstrip() + "\n\n" + new_function_code


def extract_function_descriptions(template_code):
    """
    Extracts function descriptions from the template code.

    Parameters:
    template_code (str): The Python code with docstrings.

    Returns:
    dict: A dictionary with function names as keys and their descriptions as values.
    """
    pattern = re.compile(r'def (\w+)\(.*?\):\s+"""(.*?)"""', re.DOTALL)
    return dict(pattern.findall(template_code))


def generate_and_implement_code(template_code):
    """
    Generates a complete Python codebase with given functions implemented.
    
    Parameters:
    template_code (str): The code template as a string, containing function names and their descriptions.
    
    Returns:
    tuple: A tuple containing the initial template code and the code with functions implemented.
    """
    # input(f"TEMPLATE CODE:\n{template_code}")
    if not template_code:
        return "",""

    # Use regex to extract function names and markers for pseudocode
    pattern = re.compile(r"def (\w+)\(.*?\):.*?# TODO: Implement", re.DOTALL)
    function_names = pattern.findall(template_code)
    
    code_implemented = template_code

    # Extract function names and their detailed descriptions
    function_details = extract_function_descriptions(template_code)

    # Iterate through each function and implement it
    for function_name, description in function_details.items():
        # Generate the implementation for the function
        code_implemented = implement_function(function_name, description, code_implemented)
        # input(code_implemented)

    return template_code, code_implemented
    
    
# Example usage:
function_descriptions = {
    "process_data": "This function will process the input data and return the processed data.",
    "save_results": "This function will save the given results to a file."
}
