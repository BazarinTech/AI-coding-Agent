import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return {"success": False, "message": f'Error: "{file_path}" is not in the working dir'}

    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as err:
            return {"success": False, "message": f'Could not create parent dirs {parent_dir}: {err}'}

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return {"success": True, "message": f'Successfully wrote {len(content)} characters to "{file_path}"'}
    except Exception as err:
        return {"success": False, "message": f'Failed to write to {file_path}: {err}'}


schema_write_file = {
    "name": "write_file",
    "description": "Writes or overwrites a file (creates parent dirs if needed), constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to write."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file."
            }
        },
        "required": ["file_path", "content"]
    }
}
