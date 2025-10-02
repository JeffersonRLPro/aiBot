import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    # create the paths
    abs_work = os.path.abspath(working_directory)
    full_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    # check working directory
    if not full_abs_path.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    # run the file
    if not args:
        try:
            result = subprocess.run(["python", file_path], cwd = os.path.dirname(full_abs_path), timeout = 30, capture_output = True,
                                    text = True)
        except Exception as e:
            return f'Error: executing Python file: {e}'
    else:
        try:
           result = subprocess.run(["python", file_path] + args, cwd = os.path.dirname(full_abs_path), timeout = 30, capture_output = True,
                                   text = True)
        except Exception as e:
            return f'Error: executing Python file: {e}'
    # build string
    string = ""
    try:
        stdout = result.stdout
        stdrr = result.stderr
        return_code = result.returncode
    except Exception as e:
        return f'Error: executing Python file: {e}'
    if not stdout and not stdrr:
       string += "No output produced."
    string += f"STDOUT: {stdout}\nSTDERR: {stdrr}"
    if return_code != 0:
        string += f"\nProcess exited with code {return_code}"
    return string
    

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Executes and runs a speciifc python file, it can take arguments, or no arguments. Constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to run. The file is relative to the working directory.",
            ),
        },
    ),
)
