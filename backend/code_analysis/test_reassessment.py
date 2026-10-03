from reassessment import check_answer


correct_answer = "5"

print("\n==============================")
print("TEST 1: Correct Answer")
print("==============================")

result = check_answer("5", correct_answer)
print(result)


print("\n==============================")
print("TEST 2: Wrong Answer")
print("==============================")

result = check_answer("6", correct_answer)
print(result)