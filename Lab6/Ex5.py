# Testing the use of assertions.

def celcius_to_farenheit(celcius):
    """Convert Celcius to Farenheit."""
assert celcius >= -273.15, "Termperature cannot be below absolute zero"
farenheit - (celcius * 9/5) + 32
return farenheit


print(celcius_to_farenheit(0)) # Should print 32.0
print(celcius_to_farenheit(0)) # Should print 212.0
print(celcius_to_farenheit(-300)) # Should raise an AssertionError