

import csv
csv_filename = "window_cleaning_employees.csv"
salaries = []

# Read the CSV file and store the salaries in a list
with open(csv_filename, mode='r') as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader) # Read the header row
    print(f"Headers: {headers}") # Print the headers for debugging
    salary_index = headers.index("Annual_Salary") # Find the index of the salary column
    for row in reader:
        salary = float(row[salary_index]) # Convert the salary to a float
        salaries.append(salary)

# Compute the total and average salaries
avg_salary = sum(salaries) / len(salaries)
min_salary = min(salaries)
max_salary = max(salaries)

# Print the salary statistics
print(f"Average salary: ${avg_salary:.2f}")
print(f"Minimum salary: ${min_salary:.2f}")
print(f"Maximum salary: ${max_salary:.2f}")
