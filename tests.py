from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test(title, result):
    print(title)
    indented = "\n".join("  " + line for line in result.split("\n")) if result else "  "
    print(indented)


if __name__ == "__main__":
    res1 = run_python_file("calculator", "main.py")
    test("Results of main.py:", res1)
    res2 = run_python_file("calculator", "main.py", ["3 + 5"])
    test("Results of main.py with [3+5]:", res2)
    res3 = run_python_file("calculator", "tests.py")
    test("Results of tests.py:", res3)
    res4 =  run_python_file("calculator", "../main.py")
    test("Results of ../main.py:", res4)
    res5 = run_python_file("calculator", "nonexistent.py")
    test("Results of nonexistent.py:", res5)