import os
from functions.config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    # get the full path and abs paths
    try:
        full_path = os.path.join(working_directory, file_path)
        full_abs_path = os.path.abspath(full_path)
        abs_work = os.path.abspath(working_directory)
    except:
        return "Error: The paths provided did not yield a valid path"
    if not full_abs_path.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    # check if the path is a file
    if not os.path.isfile(full_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}'
    # read file with limit
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except:
        return f'Error: Could not read file. insufficient privileges and/or not a file: {file_path}'

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Reads the first 10000 characters of a specified file, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path of the file to get the content from.",
            ),
        },
    ),
)
