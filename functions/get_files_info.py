import os
from google.genai import types

def get_files_info(working_directory, directory = "."):
    # get the full path
    full_path = os.path.join(working_directory, directory)
    # get the absolute path of full path
    absol_path_full = os.path.abspath(full_path)
    # get the absolute path of the working directory
    abs_work =  os.path.abspath(working_directory)
    # check if it is outside the working directory
    if not absol_path_full.startswith(abs_work):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # check if directory is a directory
    if not os.path.isdir(absol_path_full):
        return f'Error: "{directory}" is not a directory'
    lines = []
    # loop through the file
    try:
        for entry in os.listdir(absol_path_full):
            # build the entry path
            entry_path = os.path.join(absol_path_full, entry)
            # is it a directory
            is_dir = os.path.isdir(entry_path)
            # get the size
            file_size = os.path.getsize(entry_path)
            # build string
            lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
    except:
        return f"Error: You dont have the right previlages for {absol_path_full} or it is a file"
    return "\n".join(lines)
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)