
import subprocess
import tempfile
import os
import sys


def execute_code(code, timeout=3):
    file_path = None

    try:
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            delete=False
        ) as file:
            file.write(code)
            file_path = file.name

        # Execute using the same Python interpreter
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )

        error_message = result.stderr.strip()

        # Identify error type
        error_type = None

        if result.returncode != 0:
            if "SyntaxError" in error_message or "IndentationError" in error_message:
                error_type = "SYNTAX_ERROR"

            elif "NameError" in error_message:
                error_type = "NAME_ERROR"

            elif "TypeError" in error_message:
                error_type = "TYPE_ERROR"

            elif "ValueError" in error_message:
                error_type = "VALUE_ERROR"

            elif "IndexError" in error_message:
                error_type = "INDEX_ERROR"

            elif "KeyError" in error_message:
                error_type = "KEY_ERROR"

            elif "ZeroDivisionError" in error_message:
                error_type = "ZERO_DIVISION_ERROR"

            elif "AttributeError" in error_message:
                error_type = "ATTRIBUTE_ERROR"

            else:
                error_type = "RUNTIME_ERROR"

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": error_message,
            "error_type": error_type,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out",
            "error_type": "TIMEOUT",
            "exit_code": None
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error),
            "error_type": "EXECUTION_ERROR",
            "exit_code": None
        }

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)