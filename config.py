import dotenv
import os
import pathlib


ROOT_DIR = os.path.dirname(__file__)

env_path = os.path.join(ROOT_DIR, 'local.env')
dotenv.load_dotenv(dotenv_path=env_path)

# AGENT OPERATION
OPENAI_TOOL_MODEL = 'gpt-4-1106-preview'
OPENAI_PROMPT_MODEL = 'gpt-4-1106-preview'

# CODE GENERATION
CODE_DIR = os.path.join(ROOT_DIR, "scripts")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

OPENAI_CODE_MODEL = 'gpt-4-1106-preview'

CODE_SYSTEM_PROMPT = """\
You respond only in JSON with 1 value: "python_code"
"python_code" must be the function that is specified by the user. Provide the complete function it will be replaced in the script.

The function must be fully functional as per the specifications, and runnable out of the box.
The function must be correctly formatted.
The function must have a thorough docstring to maintain easy readability\
"""
TEMPLATE_SYSTEM_PROMPT = "Generate a Python code template with the following functions and their descriptions:\n"