import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)
        ai_action = subprocess.run(command, capture_output=True, text=True, cwd=working_dir_abs ,timeout=30)
        final_return = []
        if ai_action.returncode != 0:
            final_return.append(f"Process exited with code {ai_action.returncode}")
        if ai_action.stdout == "" and ai_action.stderr == "":
            final_return.append("No output produced")
            return "\n".join(final_return)
        final_return.append(f"STDOUT:{ai_action.stdout}")
        final_return.append(f"STDERR:{ai_action.stderr}")
        return "\n".join(final_return)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes the requested code in the python file matching the file path, using, if there are any, optional args",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the python file to execute",
                },
                "args": {
                    "type": "array",
                    "description": "optional arguments to add to the code to execute",
                    "items": {
                        "type": "string",
                        "description": "A single command-line argument"
                    }
                }
            },
            "required": [
                "file_path"
            ]
        },
    },
}





