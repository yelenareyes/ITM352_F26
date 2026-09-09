# Ask the user to enter their birth year. Calculate their age based on the current year and print it out.
# Name: Yelena Reyes
# Date: Sept. 2, 2026

birth_year = input("Enter your birth year: ")
current_year = 2026
age = current_year - int(birth_year)
age_squared = age ** 2

print("You entered:", birth_year)
print("Your age is:", age)
print("Your age squared is:", age_squared)
