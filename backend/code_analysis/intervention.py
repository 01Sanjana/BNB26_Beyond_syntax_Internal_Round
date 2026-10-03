def generate_intervention(misconception):

    misconception_id = misconception.get("id")

    if misconception_id == "PRINT_VS_RETURN":
        return {
            "concept": "print() vs return",
            "explanation": (
                "print() displays a value on the screen. "
                "return sends a value back from a function."
            ),
            "example": """def add(a, b):
    return a + b

result = add(2, 3)
print(result)""",
            "check_question": (
                "What will be stored in result after calling add(2, 3)?"
            )
        }

    if misconception_id == "LOOP_RANGE_MISCONCEPTION":
        return {
        "concept": "range() boundaries",
        "explanation": (
            "In Python, the ending value in range() is not included. "
            "For example, range(1, 4) produces 1, 2, and 3."
        ),
        "example": """for i in range(1, 4):
    print(i)""",
        "check_question": (
            "How many times will this loop execute: "
            "for i in range(1, 5)?"
        )
    }

    if misconception_id == "LIST_REFERENCE":
        return {
            "concept": "List references",
            "explanation": (
                "Assigning one list to another variable creates a reference "
                "to the same list. It does not automatically create a separate copy."
            ),
            "example": """a = [1, 2, 3]
b = a
b.append(4)

print(a)""",
            "check_question": (
                "What will be printed by the program?"
            )
        }

    return {
        "concept": "No misconception",
        "explanation": "No intervention is required.",
        "example": "",
        "check_question": ""
    }