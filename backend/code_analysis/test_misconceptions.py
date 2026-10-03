from misconception_detector import detect_misconception


test_cases = {

    "return_print_mistake": {
        "execution": {
            "success": True,
            "output": "5\nNone",
            "error": ""
        },
        "structure": {
            "valid": True,
            "loops": 0,
            "conditionals": 0,
            "functions": 1,
            "returns": 0,
            "prints": 2,
            "assignments": 1,
            "lists": 0,
            "function_calls": 3
        }
    },"loop_mistake": {
    "execution": {
        "success": True,
        "output": "1\n2\n4",
        "error": ""
    },
    "structure": {
        "valid": True,
        "loops": 1,
        "conditionals": 0,
        "functions": 0,
        "returns": 0,
        "prints": 1,
        "assignments": 0,
        "lists": 0,
        "function_calls": 2
    }
},

    "list_reference_mistake": {
        "execution": {
            "success": True,
            "output": "[1, 2, 3]",
            "error": ""
        },
        "structure": {
            "valid": True,
            "loops": 0,
            "conditionals": 0,
            "functions": 0,
            "returns": 0,
            "prints": 1,
            "assignments": 2,
            "lists": 1,
            "function_calls": 2
        }
    }
}


for name, analysis in test_cases.items():

    print("\n==============================")
    print(name)
    print("==============================")

    result = detect_misconception(analysis)

    print(result)