# Use_Module.py
# This program asks the user for two numbers, then uses HandyMath.py
# to calculate and display the midpoint, square root, exponent result,
# and the maximum and minimum values.

from HandyMath import midpoint, squareroot, max, min

# Ask the user for two numbers.
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Calculate the requested values using the functions from HandyMath.py.
mid = midpoint(num1, num2)
root = squareroot(num1 * num2)  # square root of the product of the two numbers
power_result = num1 ** num2
largest = max(num1, num2)
smallest = min(num1, num2)

# Print the results with Python f-strings for clean formatting.
print(f"The midpoint of {num1} and {num2} is: {mid}")
print(f"The square root of the product ({num1 * num2}) is: {root}")
print(f"When {num1} is raised to the exponent of {num2}, the result is: {power_result}")
print(f"The maximum of the two numbers is: {largest}")
print(f"The minimum of the two numbers is: {smallest}")
