import os
import subprocess


def run_python_file(working_directory, file_path: str, args=None):
    if args is None:
        args = []

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return {"success": False, "message": f'Cannot execute "{file_path}" as it is outside working dir'}
    if not os.path.isfile(abs_file_path):
        return {"success": False, "message": f'File "{file_path}" not found'}
    if not file_path.endswith('.py'):
        return {"success": False, "message": f'Error: "{file_path}" is not a Python file'}

    try:
        final_args = ['python3', file_path] + args
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=10,
            capture_output=True,
            text=True
        )
        return {
            "success": output.returncode == 0,
            "stdout": output.stdout,
            "stderr": output.stderr,
            "exit_code": output.returncode
        }
    except Exception as err:
        return {"success": False, "message": f'Error executing Python file: {err}'}


schema_run_python_file = {
    "name": "run_python_file",
    "description": "Runs a python file with python3 interpreter. Accepts additional CLI args as an optional array.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The file to run, relative to the working directory."
            },
            "args": {
                "type": "array",
                "description": "Optional list of CLI arguments to pass to the script.",
                "items": {"type": "string"}
            }
        },
        "required": ["file_path"]
    }
}
