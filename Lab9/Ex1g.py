import csv

with open("my_custom_sheet.csv", "r", newline="") as file_object:
    reader = csv.DictReader(file_object)
    salaries = [int(row["Annual_Salary"]) for row in reader]

print(f"Average annual salary: ${sum(salaries) / len(salaries):,.2f}")
print(f"Maximum annual salary: ${max(salaries):,}")
print(f"Minimum annual salary: ${min(salaries):,}")
