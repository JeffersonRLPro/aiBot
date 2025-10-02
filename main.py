import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, available_functions
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.write_file import write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    # get the user prompt
    user_prompt = sys.argv[1]
    # check if there is a verbose flag
    verbose = ("--verbose" in sys.argv)
    # save messages
    messages = [types.Content(role = "user", parts = [types.Part(text = user_prompt)])]
    for _ in range(0, 20):
        try:
            # get the response to test gemini
            response = client.models.generate_content(model = "gemini-2.0-flash-001", 
                contents = messages, config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            # check if verbose flag
            if verbose:
                # print the user prompt
                print(f"User prompt: {user_prompt}")
                # print token numbers
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            # print response
            function_called = response.function_calls
            if function_called:
                for function in function_called:
                    function_call_result = call_function(function, verbose)
                    # append to messages
                    generated_message = types.Content(role = "user", parts = function_call_result.parts)
                    messages.append(generated_message)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Invalid function call response")
                    #print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print(response.text)
                break
        except Exception as e:
            print(f"Error: Couldn't generate message: {e}")


def call_function(function_call_part, verbose = False):
    print(f"Calling function: {function_call_part.name}({function_call_part.args})") if verbose else print(f" - Calling function: {function_call_part.name}")
    functions = {"get_file_content": get_file_content, "run_python_file": run_python_file,
                 "get_files_info": get_files_info, "write_file": write_file}
    # check for valid function name
    if not function_call_part.name in functions:
        return types.Content(
            role = "tool",
            parts = [
                types.Part.from_function_response(
                    name = function_call_part.name,
                    response = {"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    # manually add the ./calculator working directory
    function_call_part.args["working_directory"] = "./calculator"
    # call function
    function_result = functions[function_call_part.name](**function_call_part.args)
    return types.Content(
        role = "tool",
        parts = [
            types.Part.from_function_response(
                name = function_call_part.name,
                response = {"result": function_result},
            )
        ],
    )



if __name__ == "__main__":
    main()
