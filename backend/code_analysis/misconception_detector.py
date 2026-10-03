def detect_misconception(analysis):

    execution = analysis.get("execution", {})
    structure = analysis.get("structure", {})

    output = execution.get("output", "")

    functions = structure.get("functions", 0)
    returns = structure.get("returns", 0)
    prints = structure.get("prints", 0)
    loops = structure.get("loops", 0)
    lists = structure.get("lists", 0)

    # -----------------------------------
    # 1. PRINT vs RETURN
    # -----------------------------------

    if (
        functions > 0
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
                "Output contains None"
            ]
        }

    # -----------------------------------
    # 2. LOOP / RANGE
    # -----------------------------------

    if loops > 0 and output:

        lines = output.strip().split("\n")

        # Detect a simple sequence such as:
        # 1 2 3 4
        # This may indicate that the student is
        # working with a loop, but does NOT automatically
        # mean there is a misconception.

        sequence_values = []

        for line in lines:
            try:
                sequence_values.append(int(line.strip()))
            except ValueError:
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
                    "title": "Possible range() or loop boundary misconception",
                    "explanation": (
                        "The loop output suggests that the student "
                        "may be misunderstanding the starting or ending "
                        "value of a loop."
                    ),
                    "evidence": [
                        "Loop detected",
                        "Output sequence does not match the expected consecutive sequence"
                    ]
                }

    # -----------------------------------
    # 3. LIST REFERENCE
    # -----------------------------------

    if lists > 0 and output:

        if "[" in output and "]" in output:
            return {
                "id": "LIST_REFERENCE",
                "title": "Possible list reference misconception",
                "explanation": (
                    "The student may be confusing assigning a list "
                    "reference with creating an independent copy."
                ),
                "evidence": [
                    "List detected",
                    "List output detected"
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