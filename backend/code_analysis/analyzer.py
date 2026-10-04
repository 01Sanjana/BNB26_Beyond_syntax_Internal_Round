from .executor import execute_code
from .ast_analyzer import analyze_ast


def analyze_student_code(code):
    """
    Analyze student code using AST structure and execution results.

    Returns structured evidence that can be used by the
    misconception detector and adaptive learning system.
    """

    # Analyze code structure
    try:
        ast_result = analyze_ast(code)
    except Exception as error:
        ast_result = {
            "success": False,
            "error": str(error),
            "error_type": "AST_ANALYSIS_ERROR"
        }

    # Execute student code
    execution_result = execute_code(code)

    # Combine evidence
    evidence = {
        "execution": execution_result,
        "structure": ast_result,
        "summary": {
            "execution_success": execution_result.get("success", False),
            "has_execution_error": bool(execution_result.get("error")),
            "error_type": execution_result.get("error_type"),
            "has_structure": ast_result.get("success", True)
            if isinstance(ast_result, dict)
            else True
        }
    }

    return evidence