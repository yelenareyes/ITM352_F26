searchMe = [2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]

number = int(input("Enter a number to search for: "))
found = False

for value in searchMe:
    if value == number:
        found = True
        break

if found:
    print(number, "exists in the array.")
else:
    print(number, "does not exist in the array.")


    

def is_palindrome(the_string):
    reversed_string = ""
    for character in the_string:
        reversed_string = character + reversed_string
    return the_string == reversed_string

word = input("Enter a word to check: ")

if is_palindrome(word):
    print(word, "is a palindrome.")
else:
    print(word, "is not a palindrome.")