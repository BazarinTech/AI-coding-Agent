import os


def get_files_info(working_directory, directory='.'):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working_dir, directory))

    if not abs_directory.startswith(abs_working_dir):
        return {"success": False, "message": f'Error: "{directory}" is not in the working dir'}

    try:
        contents_info = []
        contents = os.listdir(abs_directory)
        for content in contents:
            content_path = os.path.join(abs_directory, content)
            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)
            contents_info.append({
                "name": content,
                "is_dir": is_dir,
                "size": size
            })
        return {"success": True, "files": contents_info}
    except Exception as e:
        return {"success": False, "message": f"Error reading directory: {e}"}


schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory relative to the working directory (default is root of working dir)."
            }
        }
    }
}
