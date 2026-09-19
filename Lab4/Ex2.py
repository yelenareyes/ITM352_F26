
# Properly format an inputted name in title case

raw_name = input("Enter your name: ")

stripped_name = raw_name.strip()
print("Stripped name:", stripped_name)

title_case_name = stripped_name.title()
print("Formatted name in title case:", title_case_name)

# Define a list of survey response values (5, 7, 3, 8) and store them 
# in a variable. Defin ea tuple of responses IDs ((1012, 1035, 1021, and 1053).
# and add these to the list.

response_values = [5, 7, 3, 8]
response_values.sort()
response_ids = (1012, 1035, 1021, 1053)
response_values.append(response_ids)

print("Combined response values and IDs:", response_values) 

