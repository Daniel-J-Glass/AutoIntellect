import json
import re

from redbaron import RedBaron,DefNode

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
                temperature=0,
                messages=[
                        {"role": "system", "content": CODE_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                response_format={"type": "json_object"},
                timeout = 30
            )
        result = json.loads(response.choices[0].message.content)["python_code"]

    except Exception as e:
        print(e)
        result = "Coding unavailable currently, try again."
        
    return result


def generate_and_implement_code(template_code):
    """
    Generates a complete Python codebase with given functions implemented using RedBaron.
    
    Parameters:
    template_code (str): The code template as a string, containing function names and their descriptions.
    
    Returns:
    str: The code with functions implemented.
    """
    if not template_code:
        return ""
    
    red = RedBaron(template_code)

    for func_node in red.find_all('def'):
        function_name = func_node.name
        function_contents = str(func_node.value)

        if "TODO" in function_contents:
            print(f"Updating function: {function_name}")
            prompt = f"Implement the function '{function_name}' with the following context:\n\n{template_code}"
            function_code = call_llm(prompt)

            try:
                implemented_function = RedBaron(function_code)[0]

                # Extract just the body of the function
                new_function_body = implemented_function.value.dumps()
                new_function_body = new_function_body.strip()

                # # Display the new function body for debugging
                # print(f"New function body for '{function_name}':\n{new_function_body}")

                # Replace the body of the function
                func_node.value = new_function_body

                # print(f"Function '{function_name}' updated successfully.")
            except Exception as e:
                raise(f"Error processing function '{function_name}': {e}")
        # else:
        #     print(f"Skipping function: {function_name}")

    return red.dumps()


def main():
    with open("./test_code.py",'r') as f:
        template_code = f.read()

    implemented_code = generate_and_implement_code(template_code)

    with open("./test_output.py",'w') as f:
        f.write(implemented_code)

if __name__=="__main__":
    main()