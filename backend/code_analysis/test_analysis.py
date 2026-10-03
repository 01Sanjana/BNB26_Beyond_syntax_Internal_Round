from executor import execute_code


code = """
x = 10
y = 20

print(x + y)
"""

result = execute_code(code)

print(result)