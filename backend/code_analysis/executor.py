import subprocess
import tempfile
import os


def execute_code(code, timeout=3):
    file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as file:
            file.write(code)
            file_path = file.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out"
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)