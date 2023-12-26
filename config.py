import dotenv
import os
import pathlib


ROOT_DIR = os.path.dirname(__file__)

env_path = os.path.join(ROOT_DIR, 'local.env')
dotenv.load_dotenv(dotenv_path=env_path)

# GENERAL MODEL CONFIGS
CONTEXT_LEN = 4096
OUTPUT_LEN = 512
INPUT_LEN = CONTEXT_LEN-OUTPUT_LEN

# AGENT OPERATION
OPENAI_TOOL_MODEL = 'gpt-4-1106-preview'
OPENAI_PROMPT_MODEL = 'gpt-4-1106-preview'

# CODE GENERATION
CODE_DIR = os.path.join(ROOT_DIR, "scripts")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

OPENAI_CODE_MODEL = 'gpt-4-1106-preview'

CODE_SYSTEM_PROMPT = """\
You respond only in JSON with 1 value: "python_code"
"python_code" must only be the single implemented function that is specified by the user.

The function must be fully implemented as per the comments.
The function must have a thorough docstring to maintain easy readability
Pay careful attention to the structure of the code.

Do not omit any code, code as much as you can to implement the function\
"""
TEMPLATE_SYSTEM_PROMPT = "Generate a Python code template with the following functions and their descriptions:\n"