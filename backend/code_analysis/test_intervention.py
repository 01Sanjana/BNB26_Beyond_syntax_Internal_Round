from intervention import generate_intervention
from misconception_detector import detect_misconception


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


misconception = detect_misconception(analysis)

intervention = generate_intervention(misconception)

print("\nMISCONCEPTION:")
print(misconception)

print("\nPERSONALIZED INTERVENTION:")
print(intervention)