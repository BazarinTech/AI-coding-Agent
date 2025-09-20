from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
from google.genai import types

working_directory = 'calculator'


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Performing: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Performing {function_call_part.name}")

    results = ''
    if function_call_part.name == 'get_files_info':
        results = get_files_info(working_directory, **function_call_part.args)
    if function_call_part.name == 'get_file_content':
        results = get_file_content(working_directory, **function_call_part.args)
    if function_call_part.name == 'run_python_file':
        results = run_python_file(working_directory, **function_call_part.args)
    if function_call_part.name == 'write_file':
        results = write_file(working_directory, **function_call_part.args)
    if results == '':
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": results},
                )
            ],
        )
