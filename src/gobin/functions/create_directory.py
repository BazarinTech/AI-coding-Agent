import os
from rich.console import Console

console = Console()


def create_directory(path: str, verbose: bool = False):
    try:
        os.makedirs(path, exist_ok=True)
        return {"success": True, "message": f"✅ Created directory: {path}"}
    except Exception as e:
        return {"success": False, "message": f"❌ Failed to create directory: {e}"}



schema_create_directory = {
    "name": "create_directory",
    "description": "Create a new directory at the given path",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path of the directory to create"
            }
        },
        "required": ["path"]
    }
}
