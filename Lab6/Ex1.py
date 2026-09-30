emotions = ('surprise', 'sad', 'fear', 'happy')

is_it_true = emotions[-1] == "happy" and len(emotions) > 3
print(is_it_true)

# Use an if/else statement to respond to the condition.
if emotions[3] == "happy" and len(emotions) > 3:
	print(f"The fourth emotion is {emotions[3]}, and the tuple has more than three items.")
else:
	print("The condition is false.")

