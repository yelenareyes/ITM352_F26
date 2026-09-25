# Function to check the length of a list
def check_list_length(my_list):
    if len(my_list) < 5:
        print(f"List has {len(my_list)} elements: Fewer than 5 elements.")
    elif 5 <= len(my_list) <= 10:
        print(f"List has {len(my_list)} elements: Between 5 and 10 elements.")
    else:
        print(f"List has {len(my_list)} elements: More than 10 elements.")


# Example list with a variety of values
example_list = [42, "hello", 3.14, True, None]
check_list_length(example_list)


# Test cases
test_lists = [
    [1, 2, 3],                                # 3 elements
    ["a", "b", "c", "d", "e"],               # 5 elements
    [1, 2, 3, 4, 5, 6, 7, 8],               # 8 elements
    list(range(10)),                          # 10 elements
    list(range(15))                           # 15 elements
]

for test in test_lists:
    check_list_length(test)

    test_cases = [
    [],                      # 0 elements (less than 5)
    [1, 2, 3, 4],            # 4 elements (less than 5)
    [1, 2, 3, 4, 5],         # 5 elements (between 5 and 10)
    [1, 2, 3, 4, 5, 6, 7],   # 7 elements (between 5 and 10)
    list(range(10)),         # 10 elements (between 5 and 10)
    list(range(11)),         # 11 elements (more than 10)
    list(range(20))          # 20 elements (more than 10)
]

for case in test_cases:
    check_list_length(case)

    def run_tests(test_cases):
    for case in test_cases:
        check_list_length(case)

run_tests(test_cases)