from learning_flow import run_learning_flow


analysis = {
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
}


print("\n==============================")
print("CASE 1: Student understands")
print("==============================")


result = run_learning_flow(
    analysis,
    "5",
    "5"
)

print(result)


print("\n==============================")
print("CASE 2: Student still confused")
print("==============================")


result = run_learning_flow(
    analysis,
    "6",
    "5"
)

print(result)