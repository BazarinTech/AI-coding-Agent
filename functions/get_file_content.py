import os
from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    file_get_content_string = ''
    try:
        with open(abs_file_path, 'r') as f:
            file_get_content_string = f.read(MAX_CHARS)
            if len(file_get_content_string) >= MAX_CHARS:
                file_get_content_string += (
                    f'[...File "{file_path} trancated at 1000 characters]'
                )
        return file_get_content_string
    except Exception as err:
        return f'Exception reading file {err}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the given files as string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file, from the working directory.",
            ),
        },
    ),
)
