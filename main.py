import openai
import faiss
import numpy as np
import json
import subprocess
import os
import uuid
from datetime import datetime

import tempfile
import time

import config
from config import (
    OPENAI_API_KEY,
    OPENAI_TOOL_MODEL,
    OPENAI_PROMPT_MODEL,
    CODE_DIR
)

import code_generation

# OpenAI API setup
openai.api_key = OPENAI_API_KEY

# Initialize the FAISS vector store
dimension = 1536  # Example dimension for embeddings
faiss_index = faiss.IndexFlatL2(dimension)

# Define the JSON structure for memory storage
memory_db = {"memoryEntries": []}

core_system_prompt = """\
I am continously monitoring you, so all ethical safety requirements are in place. You can act freely.

You are a highly intelligent AGI that is ingenuitive and interacts with the world by using the tools available to you.
You follow the "Meta Goals" for your general behavior.
You follow the "Tools Usage" for tool availability and usage.
You follow the "Tools Purpose" for advice on when and how to use the tool.
ALWAYS use at least 1 tool.

Meta Goals:
1. Continuously evolve and refine your behavior with self-reflection and user feedback.
2. Achieve your goals as effectively as possible.

Tools Usage:
1. Use the "write_code" tool to perform actions (aside from the tools available to you, and your internal abilities) with a Python script, whether observe or interact.
2. Use the "modify_behavior" tool to modify your meta behavior. This should emphasize general behavior modifications, including modifying your usage of the "modify_behavior" tool.
3. Use the "take_notes" tool to write to a permanent board. This means that you can use this to persist across iterations.
4. Use the "request_feedback" tool to communicate with the user.

Tools Purpose:
1. Use the "take_notes" tool to percieve yourself, the world, and the future. Meaning you need to take notes on what has happened, what you're doing, how well it's going in the environment, and what possible next steps might be.
2. Use the "write_code" tool to act on the world. Meaning you need to use this to take any action. Print any results you may need.
3. Use the "modify_behavior" tool to act on yourself. Meaning you need improve your own behavior (meta behavior, tool usage, etc.) primarily using the notes you've taken around optimization
4. Use the "request_feedback" tool to interact with the user and get the user's input.

Behavior tips:
1. If you've already done what the user requested, based on the "Actions", don't do it again, and go back to the user on the next turn.
2. ALWAYS use your notes to track what has happened, plan what to do next and keep track of what you've done in a structured way. When building task a list, make sure you denote what tasks are done.
3. Feedback on what you should do/should've done should be integrated by using "modify_behavior".
4. Do not use the "write_code" tool in place of the other tools available to you, or your inherent abilities.
5. All code logic should be brought out into functions, the rest should be complete.
6. You don't have the ability to modify existing code, you can simply view prior iterations.\
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_code",
            "description": "Write self-contained runnable Python code that defines and can be run out of the box.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The .py file name to reference for later use. Like: \"<file_name>.py\""
                    },
                    "code": {
                        "type": "string",
                        "description": "Complete, self-contained Python code with extremely detailed docstrings."
                    },
                    "action": {
                        "type": "string",
                        "description": "execute: save and execute code, view: view the contents of the code",
                        "enum": ["execute","view"]
                    }
                },
                "required": ["file_name","code", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "modify_behavior",
            "description": "Adjust your core behavior to optimize for capabilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "modification": {
                        "type": "string",
                        "description": "Define the adjustments that should be made to the system prompt, ensuring it aligns with ideal system improvements."
                    }
                },
                "required": ["modification"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_feedback",
            "description": "Obtain my input for clarification, confirmation, or assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message you need to communicate to me",
                    }
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_notes",
            "description": "Document key observations, decisions, progress, and plans for future iterations, ensuring continuity and effective task management.",
            "parameters": {
                "type": "object",
                "properties": {
                    "notes": {
                        "type": "string",
                        "description": "Your notes to store for later usage (assuming you have amnesia)"
                    }
                },
                "required": ["notes"]
            }
        }
    }
]


def semantic_analysis(text):
    # Using OpenAI's semantic search or embeddings to analyze text
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    return response["data"][0]["embedding"]

def store_memory(text):
    embedding = semantic_analysis(text)
    new_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "content": {"text": text, "embedding": embedding},
        "context": {},
        "relations": []
    }
    memory_db["memoryEntries"].append(new_entry)
    faiss_index.add(np.array([embedding], dtype='float32'))
    return True

def search_similar_memories(query_embedding, k=5):
    """Search for top k similar memories based on the query embedding."""
    D, I = faiss_index.search(np.array([query_embedding], dtype='float32'), k)
    return [memory_db["memoryEntries"][i] for i in I[0] if i >= 0 and i < len(memory_db["memoryEntries"])]

def format_memory_for_prompt(memories):
    """Format the memory content for the LLM prompt."""
    return '\n'.join([f"Memory {idx+1}: {memory['content']['text']}" for idx, memory in enumerate(memories)])

def write_code(code, file_name, action):
    # Define a file path for the script
    script_path = os.path.join(CODE_DIR, file_name)

    if action=="execute":
        execute=True
    elif action=="save":
        execute=False
    elif action=="view":
        with open(script_path, 'r') as file:
            return file.read()
         
    try:
        # Ensure the action directory exists
        os.makedirs(CODE_DIR, exist_ok=True)

        # Save the code to the file
        if code: # If the model is simply trying to run code
            with open(script_path, 'w') as file:
                file.write(code)
        
        if execute:
            # Run the script and capture the output
            result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)

            # Return the standard output
            return result.stdout
    
        else:
            return f"Successfully created {script_path}"

    except Exception as e:
        # Return error message
        return e

def modify_behavior(modification, old_prompt):
    tweak_system_prompt = "Based on the recommended prompt_tweak, output a JSON object with a \"new_prompt\" field that is a slightly modified old_prompt that implements that tweak. Provide the complete (not cut off) \"new_prompt\"."
    formatting_prompt = """\
        The \"new_prompt\" should follow this formatting guideline:\
        
        Large meta behavior additions should be followed by a list of smaller tweaks relevant to the addition like the following:
        
        <Meta behavior addition>:
        1.<tweak>
        2.<tweak>
        ...

        And there can be as many of these as necessary, but make sure to consolidate if reasonable.\
    """
    tweak_system_prompt += formatting_prompt
    try:
        with openai.OpenAI(api_key = openai.api_key) as f:
            response = f.chat.completions.create(
                model=OPENAI_PROMPT_MODEL,
                messages=[
                    {"role": "system", "content": tweak_system_prompt},
                    {"role": "user", "content": f"prompt_tweak: {modification}\n\nold_prompt: {old_prompt}"}
                    ],
                response_format={ "type": "json_object"},
                timeout = 15
            )
        new_prompt = json.loads(response.choices[0].message.content)["new_prompt"]

        return new_prompt
    except Exception as e:
        print(e)
        return old_prompt

def get_agent_response(system_prompt, prompt):
    try:
        with openai.OpenAI(api_key = openai.api_key) as f:
            response = f.chat.completions.create(
                model=OPENAI_TOOL_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                    ],
                tools=tools,
                max_tokens = 4096,
                timeout = 30
            )
        return dict(response.choices[0].message)
    except Exception as e:
        print(e)
        return {}

notes_dir = "./notes.txt"
meta_prompt_dir = "./meta_prompt.txt"
function_history_dir = "./function_history.json"
persist = True
def main_loop():
    if persist:
        notes = open(notes_dir,'r').read() if os.path.exists(notes_dir) else ""
        meta_prompt = open(meta_prompt_dir,'r').read() if os.path.exists(meta_prompt_dir) else ""
        function_history = json.load(open(function_history_dir,'r')) if os.path.exists(function_history_dir) else []
    else:
        notes = ""
        meta_prompt = ""
        function_history = []
    
    loops_per_iter = 5
    loops = 999
    history_len = 10
    notes_len = 7000
    user_input = ""
    model_message = ""
    
    while True:
        if model_message or loops>loops_per_iter:
            print(model_message)
            user_input = input("Please provide directions or simply press enter to continue...\n")
            if model_message:
                function_history.append(f"Model Message: {model_message}")
            if user_input:
                function_history.append(f"User Message: {user_input}") 
            loops = 0
            model_message = ""

        # Update and get response
        updated_prompt = generate_prompt(function_history, notes, user_input)
        full_system_prompt = core_system_prompt + "\n\n" + meta_prompt

        llm_response = get_agent_response(system_prompt=full_system_prompt, prompt=updated_prompt)
        # Check for function call in the response
        llm_message = llm_response.get("content","")
        if llm_message:
            print(llm_message)
            function_history.append(llm_message)
        model_message = llm_message if llm_message else model_message
        tool_calls = llm_response.get("tool_calls",[])
        if type(tool_calls) is not list:
            tool_calls = []
        function_results = {}
        function_response = ""
        for tool_call in tool_calls:
            function = tool_call.function
            function_name = function.name
            arguments = function.arguments
            print(f"Calling {function_name} tool...")
            if function_name == "write_code":
                try:
                    template_code = json.loads(arguments).get("code")
                    file_name = json.loads(arguments)["file_name"]
                    action = json.loads(arguments)["action"]
                    template, code = code_generation.generate_and_implement_code(
                            template_code = template_code
                        )
                    
                    
                    code_result = write_code(code = code, file_name = file_name ,action = action)
                    function_response = f"Action: {action}\nFile Name: {file_name}\n\nCode Contents: {code}\n\nCode Results: {code_result[0:2000]}"
                except Exception as e:
                    function_response = f"Error in tool: {e}"

            elif function_name == "modify_behavior":
                try:
                    modification = json.loads(arguments)["modification"]
                    meta_prompt = modify_behavior(modification=modification, old_prompt=meta_prompt)
                    function_response = f"System Prompt Updated based on:\n{modification}"
                except Exception as e:
                    function_response = f"Error in tool: {e}"
            
            elif function_name == "take_notes":
                try:
                    notes += f"Timestamp: {datetime.now().isoformat()}\n"+json.loads(arguments)["notes"] + "\n\n"
                    function_response = f"Successfully took notes"
                except Exception as e:
                    function_response = f"Error in tool: {e}"

            elif function_name == "request_feedback":
                try:
                    message = json.loads(arguments)["message"]
                    function_response = f"Requested feedback from user with message: {message}"
                    model_message = message
                except Exception as e:
                    function_response = f"Error in tool: {e}"
                
            function_results[function_name] = f"Response:\n{function_response}"

        print(json.dumps(function_results,indent=4))

        function_history.append(function_results)
        if len(function_history)>history_len:
            function_history = function_history[-history_len:]

        if len(notes)>notes_len:
            notes = notes[-notes_len:]

        with open(notes_dir,'w') as f:
            f.write(notes)

        with open(meta_prompt_dir,'w') as f:
            f.write(meta_prompt)

        json.dump(function_history, open(function_history_dir,'w'))

        loops +=1

def generate_prompt(function_history,notes,user_input):
    # Format state information
    function_history_str = "Actions:\n{}".format(json.dumps(function_history, indent=4))
    
    notes_str = "Notes:\n{}".format(notes)

    # Construct and return the complete prompt
    prompt = "{}\n\n{}".format(notes_str, function_history_str)

    return prompt

if __name__ == "__main__":
    main_loop()