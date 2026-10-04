
from executor import execute_code


test_cases = [
    {
        "name": "Correct Code",
        "code": "print(10 + 20)",
        "expected": None
    },
    {
        "name": "Syntax Error",
        "code": "print(10",
        "expected": "SYNTAX_ERROR"
    },
    {
        "name": "Name Error",
        "code": "print(undefined_variable)",
        "expected": "NAME_ERROR"
    },
    {
        "name": "Type Error",
        "code": "print('10' + 5)",
        "expected": "TYPE_ERROR"
    },
    {
        "name": "Zero Division",
        "code": "print(10 / 0)",
        "expected": "ZERO_DIVISION_ERROR"
    },
    {
        "name": "Index Error",
        "code": "numbers = [1, 2]\nprint(numbers[5])",
        "expected": "INDEX_ERROR"
    },
    {
        "name": "Timeout",
        "code": "while True:\n    pass",
        "expected": "TIMEOUT"
    }
]


for test in test_cases:
    print("\n==============================")
    print(test["name"])
    print("==============================")

    result = execute_code(test["code"], timeout=2)

    print(result)

    if test["expected"] is None:
        assert result["success"] is True
    else:
        assert result["success"] is False
        assert result["error_type"] == test["expected"]

    print("TEST PASSED")


print("\nAll executor tests passed!")