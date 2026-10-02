data = ("hello", 10, "goodbye", 3, "goodnight", 5)
new_item = input("Enter a value to add to the tuple: ")

print("Original tuple:", data)

try:
	data.append(new_item)
except AttributeError as error:
	print(f"An attempt was made to append {new_item!r} to the tuple.")
	print("Error:", error)

# Indexing accesses an existing item; it does not make a tuple mutable.

tuple_with_item = data + (new_item,)
print("Using tuple concatenation:", tuple_with_item)

tuple_with_item = (*data, new_item)
print("Using unpacking:", tuple_with_item)

data_list = list(data)
data_list.append(new_item)
tuple_with_item = tuple(data_list)
print("Using list.append():", tuple_with_item)
