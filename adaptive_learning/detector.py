def detect_misconception(code, expected_output, student_output):
    """
    Detect a likely programming misconception
    from the student's code and output.
    """

    # Reference vs copy
    if "y = x" in code and ".append(" in code:
        if student_output != expected_output:
            return "reference_vs_copy"

    # Off-by-one
    if "range(" in code:
        if student_output != expected_output:
            return "off_by_one"

    # Print vs return
    if "def " in code and "print(" in code:
        if "return" not in code:
            return "print_vs_return"

    return None