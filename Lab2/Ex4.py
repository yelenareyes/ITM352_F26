# Ask the user to enter a decimal number. Calculate the square of that number
# round it to two decimal places and print it out.
# Name: Yelena Reyes
# Date: Sept. 2, 2026

input_value = input("Enter a floating-point number: ")
float_value = float(input_value)
squared_value = float_value ** 2
rounded_value = round(squared_value, 2)

print("You entered:", float_value)
print("The square of the number you entered is:", squared_value, 'Have a nice day!')
