def detect_misconception(analysis):

    execution = analysis.get("execution", {})
    structure = analysis.get("structure", {})
    summary = analysis.get("summary", {})

    output = execution.get("output", "")

    functions = structure.get("functions", 0)
    returns = structure.get("returns", 0)
    prints = structure.get("prints", 0)
    loops = structure.get("loops", 0)
    lists = structure.get("lists", 0)

    execution_success = summary.get(
        "execution_success",
        execution.get("success", True)
    )

    # -----------------------------------
    # 1. PRINT vs RETURN
    # -----------------------------------

    if (
        execution_success
        and functions > 0
        and returns == 0
        and prints >= 2
        and "None" in output
    ):
        return {
            "id": "PRINT_VS_RETURN",
            "title": "Confusing print() and return",
            "explanation": (
                "The function prints a value but does not return it. "
                "print() displays a value, while return sends a value "
                "back to the caller."
            ),
            "evidence": [
                "Function detected",
                "No return statement detected",
                "Output contains None",
                "Execution completed successfully"
            ]
        }

    # -----------------------------------
    # 2. LOOP / RANGE
    # -----------------------------------

    if execution_success and loops > 0 and output:

        lines = output.strip().splitlines()
        sequence_values = []

        for line in lines:
            try:
                sequence_values.append(int(line.strip()))
            except ValueError:
                sequence_values = []
                break

        if len(sequence_values) >= 2:

            expected = list(
                range(
                    sequence_values[0],
                    sequence_values[-1] + 1
                )
            )

            if sequence_values != expected:
                return {
                    "id": "LOOP_RANGE_MISCONCEPTION",
                    "title": (
                        "Possible range() or loop boundary misconception"
                    ),
                    "explanation": (
                        "The loop output suggests that the student "
                        "may be misunderstanding the starting or ending "
                        "value of a loop."
                    ),
                    "evidence": [
                        "Loop detected",
                        "Output sequence does not match the expected "
                        "consecutive sequence",
                        "Execution completed successfully"
                    ]
                }

    # -----------------------------------
    # 3. LIST REFERENCE
    # -----------------------------------

    if execution_success and lists > 0 and output:

        if "[" in output and "]" in output:
            return {
                "id": "LIST_REFERENCE",
                "title": "Possible list reference misconception",
                "explanation": (
                    "The student may be confusing assigning a list "
                    "reference with creating an independent copy. "
                    "More evidence is needed to confirm this."
                ),
                "evidence": [
                    "List detected",
                    "List output detected",
                    "Potential reference misconception"
                ]
            }

    # -----------------------------------
    # 4. EXECUTION ERROR
    # -----------------------------------

    if not execution_success:
        return {
            "id": "NONE",
            "title": "Execution error detected",
            "explanation": (
                "The submitted code could not complete successfully. "
                "The error should be reviewed before identifying "
                "a specific conceptual misconception."
            ),
            "evidence": [
                "Execution failed",
                "Error type: " + str(
                    execution.get("error_type", "UNKNOWN")
                ),
                execution.get("error", "No error details available")
            ]
        }

    # -----------------------------------
    # NO KNOWN MISCONCEPTION
    # -----------------------------------

    return {
        "id": "NONE",
        "title": "No known misconception detected",
        "explanation": (
            "The current analysis does not provide enough evidence "
            "for a known misconception."
        ),
        "evidence": []
    }