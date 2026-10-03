from executor import execute_code
from ast_analyzer import analyze_ast


def analyze_student_code(code):
    ast_result = analyze_ast(code)
    execution_result = execute_code(code)

    evidence = {
        "execution": execution_result,
        "structure": ast_result
    }

    return evidence