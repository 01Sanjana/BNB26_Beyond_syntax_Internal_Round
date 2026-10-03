from analyzer import analyze_student_code


tests = {
    "correct_code": """
x = 10
y = 20
print(x + y)
""",

    "loop_mistake": """
for i in range(1, 5):
    print(i)
""",

    "return_print_mistake": """
def add(a, b):
    print(a + b)

result = add(2, 3)
print(result)
""",

    "list_reference_mistake": """
x = [1, 2]
y = x
y.append(3)

print(x)
"""
}


for name, code in tests.items():

    print("\n==============================")
    print(name)
    print("==============================")

    result = analyze_student_code(code)

    print(result)