import ast


def analyze_ast(code):

    try:
        tree = ast.parse(code)

    except SyntaxError as e:
        return {
            "valid": False,
            "syntax_error": str(e)
        }

    analysis = {
        "valid": True,
        "loops": 0,
        "conditionals": 0,
        "functions": 0,
        "returns": 0,
        "prints": 0,
        "assignments": 0,
        "lists": 0,
        "function_calls": 0
    }

    for node in ast.walk(tree):

        if isinstance(node, (ast.For, ast.While)):
            analysis["loops"] += 1

        elif isinstance(node, ast.If):
            analysis["conditionals"] += 1

        elif isinstance(node, ast.FunctionDef):
            analysis["functions"] += 1

        elif isinstance(node, ast.Return):
            analysis["returns"] += 1

        elif isinstance(node, ast.Assign):
            analysis["assignments"] += 1

        elif isinstance(node, ast.List):
            analysis["lists"] += 1

        elif isinstance(node, ast.Call):
            analysis["function_calls"] += 1

            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    analysis["prints"] += 1

    return analysis