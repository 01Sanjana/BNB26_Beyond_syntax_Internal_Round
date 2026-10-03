from detector import detect_misconception


# Test 1: Reference vs Copy
code = """x = [1, 2, 3]
y = x
y.append(4)
print(x)"""

result = detect_misconception(
    code,
    "[1, 2, 3]",
    "[1, 2, 3, 4]"
)

print("Test 1:", result)


# Test 2: Off by One
code = """for i in range(5):
    print(i)"""

result = detect_misconception(
    code,
    "0\n1\n2\n3\n4",
    "0\n1\n2\n3"
)

print("Test 2:", result)


# Test 3: Print vs Return
code = """def add(a, b):
    print(a + b)

result = add(2, 3)"""

result = detect_misconception(
    code,
    "5",
    "None"
)

print("Test 3:", result)