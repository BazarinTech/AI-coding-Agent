from .functions.get_files_info import get_files_info
from .functions.get_file_content import get_file_content
from .functions.run_python import run_python_file
from .functions.write_file import write_file
from .functions.run_shell import run_shell_command
from .functions.create_directory import create_directory
from google.genai import types
import os

working_directory = os.getcwd()

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Performing: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Performing {function_call_part.name}")

    result = None

    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)

    elif function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)

    elif function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)

    elif function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)

    elif function_call_part.name == "run_shell_command":
        result = run_shell_command(**function_call_part.args, verbose=verbose)

    elif function_call_part.name == "create_directory":
        args = function_call_part.args or {}
        result = create_directory(args.get("path"), verbose)

    else:
        result = {"error": f"Unknown function: {function_call_part.name}"}

    # Always wrap result in one function_response part
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=result,  # 👈 plain dict or string
            )
        ],
    )
