import re
from typing import Any, Dict, List


# ============================================================
# RE:LEARN - ALGEBRA MISCONCEPTION DETECTION ENGINE
# Member 1: ML / Misconception Detection
# ============================================================

MISCONCEPTIONS = {
    "M1": {
        "name": "Sign Error",
        "description": (
            "Student mishandles a positive or negative sign "
            "while rearranging an equation."
        )
    },

    "M2": {
        "name": "Distributive Property Error",
        "description": (
            "Student fails to distribute a coefficient "
            "to every term inside parentheses."
        )
    },

    "M3": {
        "name": "Equation Balancing Error",
        "description": (
            "Student changes one side of an equation "
            "without making the equivalent change to the other side."
        )
    },

    "M4": {
        "name": "Fraction Operation Error",
        "description": (
            "Student incorrectly adds, subtracts, multiplies, "
            "or simplifies fractions."
        )
    },

    "M5": {
        "name": "Variable/Constant Confusion",
        "description": (
            "Student treats unlike terms, such as a variable term "
            "and a constant, as if they were like terms."
        )
    },

    "M6": {
        "name": "Exponent Rule Error",
        "description": (
            "Student applies an incorrect rule when simplifying powers."
        )
    }
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(text: str) -> str:
    """Normalize text for easier pattern matching."""

    return (
        text.lower()
        .strip()
        .replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace(" ", "")
    )


def extract_steps(student_solution: str) -> List[str]:
    """Split a multi-line student solution into individual steps."""

    return [
        line.strip()
        for line in student_solution.splitlines()
        if line.strip()
    ]


def make_result(
    misconception_id: str,
    confidence: float,
    evidence: List[str]
) -> Dict[str, Any]:
    """Create a standard misconception diagnosis."""

    info = MISCONCEPTIONS[misconception_id]

    return {
        "status": "misconception_detected",
        "misconception_id": misconception_id,
        "misconception": info["name"],
        "confidence": round(confidence, 2),
        "evidence": evidence,
        "description": info["description"]
    }


def no_misconception() -> Dict[str, Any]:
    """Return result when no known misconception is detected."""

    return {
        "status": "no_known_misconception",
        "misconception_id": None,
        "misconception": None,
        "confidence": 0.0,
        "evidence": [],
        "description": (
            "No known misconception was detected "
            "from the submitted solution."
        )
    }


# ============================================================
# M1 - SIGN ERROR
# ============================================================

def detect_sign_error(question: str, student_solution: str):
    """
    Detect common sign mistakes while rearranging equations.

    Example:
        x + 5 = 10
        x = 10 + 5      -> wrong
    """

    q = normalize(question)
    steps = extract_steps(student_solution)

    match = re.fullmatch(r"x([+-])(\d+)=(-?\d+)", q)

    if not match:
        return None

    operator = match.group(1)
    constant = int(match.group(2))
    rhs = int(match.group(3))

    for step in steps[1:]:
        normalized_step = normalize(step)

        if not normalized_step.startswith("x="):
            continue

        value = normalized_step[2:]

        wrong_form = f"{rhs}{operator}{constant}"

        if value == wrong_form:

            expected = (
                rhs - constant
                if operator == "+"
                else rhs + constant
            )

            return make_result(
                "M1",
                0.95,
                [
                    (
                        f"The constant {constant} should change sign "
                        "when moved across the equation."
                    ),
                    (
                        f"The student wrote "
                        f"x = {rhs} {operator} {constant}."
                    ),
                    f"Expected value: x = {expected}."
                ]
            )

    return None


# ============================================================
# M2 - DISTRIBUTIVE PROPERTY ERROR
# ============================================================

def detect_distributive_error(question: str, student_solution: str):
    """
    Detect failure to distribute a coefficient
    to every term inside parentheses.

    Example:
        2(x + 3) = 14
        2x + 3 = 14    -> wrong
    """

    q = normalize(question)
    s = normalize(student_solution)

    match = re.fullmatch(
        r"(\d+)\(([a-z])([+-])(\d+)\)=(-?\d+)",
        q
    )

    if not match:
        return None

    coefficient = int(match.group(1))
    variable = match.group(2)
    operator = match.group(3)
    constant = int(match.group(4))

    correct_constant = coefficient * constant

    wrong_part = (
        f"{coefficient}{variable}"
        f"{operator}{constant}"
    )

    correct_part = (
        f"{coefficient}{variable}"
        f"{operator}{correct_constant}"
    )

    if wrong_part in s and correct_part not in s:

        return make_result(
            "M2",
            0.96,
            [
                (
                    f"The coefficient {coefficient} "
                    f"was applied to {variable}."
                ),
                (
                    f"It was not distributed to "
                    f"the constant {constant}."
                ),
                (
                    f"The constant should become "
                    f"{correct_constant}."
                )
            ]
        )

    return None


# ============================================================
# M3 - EQUATION BALANCING ERROR
# ============================================================

def detect_balance_error(question: str, student_solution: str):
    """
    Detect when only one side of an equation changes.

    Example:
        3x + 5 = 20
        3x = 20         -> wrong
    """

    steps = extract_steps(student_solution)

    equations = []

    for step in steps:

        if "=" not in step:
            continue

        left, right = step.split("=", 1)

        equations.append(
            (
                normalize(left),
                normalize(right)
            )
        )

    if len(equations) < 2:
        return None

    for previous, current in zip(
        equations,
        equations[1:]
    ):

        previous_left, previous_right = previous
        current_left, current_right = current

        left_changed = previous_left != current_left
        right_changed = previous_right != current_right

        # Only left side changed
        if left_changed and not right_changed:

            return make_result(
                "M3",
                0.93,
                [
                    (
                        f"Previous step: "
                        f"{previous_left} = {previous_right}"
                    ),
                    (
                        f"Student step: "
                        f"{current_left} = {current_right}"
                    ),
                    (
                        "The left side changed while "
                        "the right side stayed unchanged."
                    ),
                    (
                        "The same equivalent operation "
                        "must be applied to both sides."
                    )
                ]
            )

        # Only right side changed
        if right_changed and not left_changed:

            return make_result(
                "M3",
                0.93,
                [
                    (
                        f"Previous step: "
                        f"{previous_left} = {previous_right}"
                    ),
                    (
                        f"Student step: "
                        f"{current_left} = {current_right}"
                    ),
                    (
                        "The right side changed while "
                        "the left side stayed unchanged."
                    ),
                    (
                        "The same equivalent operation "
                        "must be applied to both sides."
                    )
                ]
            )

    return None


# ============================================================
# M4 - FRACTION OPERATION ERROR
# ============================================================

def detect_fraction_error(question: str, student_solution: str):
    """
    Detect classic fraction addition misconception.

    Example:
        1/2 + 1/3 = 2/5
    """

    s = normalize(student_solution)

    match = re.search(
        r"(\d+)/(\d+)\+(\d+)/(\d+)=(\d+)/(\d+)",
        s
    )

    if not match:
        return None

    a, b, c, d, result_num, result_den = map(
        int,
        match.groups()
    )

    if result_num == a + c and result_den == b + d:

        return make_result(
            "M4",
            0.97,
            [
                (
                    "The student added the numerators "
                    "and denominators directly."
                ),
                (
                    "Fractions with different denominators "
                    "require a common denominator."
                )
            ]
        )

    return None


# ============================================================
# M5 - VARIABLE / CONSTANT CONFUSION
# ============================================================

def detect_variable_constant_confusion(
    question: str,
    student_solution: str
):
    """
    Detect treating unlike terms as like terms.

    Example:
        2x + 3 = 5x   -> wrong reasoning
    """

    s = normalize(student_solution)

    match = re.search(
        r"(\d+)x\+(\d+)=(-?\d+)x",
        s
    )

    if match:

        return make_result(
            "M5",
            0.90,
            [
                (
                    "A variable term and a constant "
                    "were treated as if they were like terms."
                ),
                "Only like terms can be combined.",
                (
                    "For example, 2x and 3 "
                    "cannot be directly combined."
                )
            ]
        )

    return None


# ============================================================
# M6 - EXPONENT RULE ERROR
# ============================================================

def detect_exponent_error(question: str, student_solution: str):
    """
    Detect incorrect exponent manipulation.

    Examples:
        x^2 * x^3 = x^6    -> wrong
        x^2 + x^3 = x^5    -> wrong
    """

    s = normalize(student_solution)

    # --------------------------------------------------------
    # Multiplication of powers
    # x^2 * x^3 = x^6
    # --------------------------------------------------------

    match = re.search(
        r"x\^(\d+)\*x\^(\d+)=x\^(\d+)",
        s
    )

    if match:

        a, b, result = map(
            int,
            match.groups()
        )

        if result == a * b and result != a + b:

            return make_result(
                "M6",
                0.96,
                [
                    "The student multiplied the exponents.",
                    (
                        f"For x^{a} × x^{b}, "
                        "the exponents should be added."
                    ),
                    f"Expected exponent: {a + b}."
                ]
            )

    # --------------------------------------------------------
    # Addition of powers
    # x^2 + x^3 = x^5
    # --------------------------------------------------------

    match = re.search(
        r"x\^(\d+)\+x\^(\d+)=x\^(\d+)",
        s
    )

    if match:

        a, b, result = map(
            int,
            match.groups()
        )

        if result == a + b:

            return make_result(
                "M6",
                0.93,
                [
                    (
                        "The student added exponents "
                        "while adding two terms."
                    ),
                    (
                        "Exponents are not combined this way "
                        "when terms are added."
                    )
                ]
            )

    return None


# ============================================================
# MAIN MISCONCEPTION ENGINE
# ============================================================

def detect_misconception(
    question: str,
    student_solution: str
) -> Dict[str, Any]:
    """
    Main function used by the frontend/backend.

    Input:
        question
        student_solution

    Output:
        misconception
        confidence
        evidence
        status
    """

    if not question or not student_solution:

        return {
            "status": "invalid_input",
            "misconception_id": None,
            "misconception": None,
            "confidence": 0.0,
            "evidence": [
                "Question and student solution are required."
            ],
            "description": ""
        }

    detectors = [
        detect_sign_error,
        detect_distributive_error,
        detect_balance_error,
        detect_fraction_error,
        detect_variable_constant_confusion,
        detect_exponent_error
    ]

    detected_results = []

    for detector in detectors:

        result = detector(
            question,
            student_solution
        )

        if result is not None:
            detected_results.append(result)

    if detected_results:

        # Return strongest diagnosis
        return max(
            detected_results,
            key=lambda result: result["confidence"]
        )

    return no_misconception()


# ============================================================
# LOCAL TESTING
# ============================================================

if __name__ == "__main__":

    test_cases = [

        {
            "name": "Distributive Property Error",
            "question": "2(x + 3) = 14",
            "student_solution": "2x + 3 = 14"
        },

        {
            "name": "Sign Error",
            "question": "x + 5 = 10",
            "student_solution": (
                "x + 5 = 10\n"
                "x = 10 + 5"
            )
        },

        {
            "name": "Equation Balancing Error",
            "question": "3x + 5 = 20",
            "student_solution": (
                "3x + 5 = 20\n"
                "3x = 20"
            )
        },

        {
            "name": "Fraction Operation Error",
            "question": "1/2 + 1/3",
            "student_solution": (
                "1/2 + 1/3 = 2/5"
            )
        },

        {
            "name": "Variable / Constant Confusion",
            "question": "2x + 3",
            "student_solution": (
                "2x + 3 = 5x"
            )
        },

        {
            "name": "Exponent Rule Error",
            "question": "x^2 * x^3",
            "student_solution": (
                "x^2 * x^3 = x^6"
            )
        }
    ]

    print()
    print("=" * 70)
    print("RE:LEARN ALGEBRA MISCONCEPTION ENGINE")
    print("=" * 70)
    print()

    for number, case in enumerate(
        test_cases,
        start=1
    ):

        result = detect_misconception(
            case["question"],
            case["student_solution"]
        )

        print(f"Test Case {number}: {case['name']}")
        print("Question :", case["question"])
        print("Student  :", case["student_solution"])
        print("Result   :", result)
        print("-" * 70)