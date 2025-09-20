import os
from gobin.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return {"success": False, "message": f'Error: "{file_path}" is not in the working dir'}
    if not os.path.isfile(abs_file_path):
        return {"success": False, "message": f'Error: "{file_path}" is not a file'}

    try:
        with open(abs_file_path, 'r') as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return {"success": True, "content": file_content}
    except Exception as err:
        return {"success": False, "message": f'Exception reading file {err}'}


schema_get_file_content = {
    "name": "get_file_content",
    "description": "Gets the content of the given files as string, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to file, from the working directory."
            }
        },
        "required": ["file_path"]
    }
}
