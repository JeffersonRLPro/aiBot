import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # create paths
    try:
        abs_work = os.path.abspath(working_directory)
        full_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        dir_path = os.path.dirname(full_abs_path)
    except:
        return f'Error: The created path was invalid: {working_directory}, {file_path}'
    # check if outside
    if not full_abs_path.startswith(abs_work):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # check if it exist
    if not os.path.exists(full_abs_path):
        # create a new file
        try:
            os.makedirs(dir_path, exist_ok = True)
        except Exception as e:
            return f'Error: Couldnt create a directory/file {e}'
    # check if file
    if os.path.exists(full_abs_path) and os.path.isdir(full_abs_path):
        return f'Error: "{file_path}" is a directory, not a file'
    # write to the file
    try:
        with open(full_abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing to file: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specific file, if file not found, then it makes a new file in the specified directory. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The name of the file that was provided. the file is relative to the working directory.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The content to write to the file provided."
            ),
        },
    ),
)