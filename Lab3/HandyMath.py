# HandyMath.py

def midpoint(num1, num2):
    return (num1 + num2) / 2

def squareroot(number):
    return number ** 0.5

def exponent(base, power):
    return base ** power

def max(num1, num2):
    return num1 if num1 > num2 else num2

def min(num1, num2):
    return num1 if num1 < num2 else num2


# Extra Credit Function
def function_report(x, y, func):
    return f"The function {func.__name__}({x}, {y}) = {func(x, y)}"
    