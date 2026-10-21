# Open a file and read its contents

with open("names.txt", "r") as file_object:
    contents = file_object.read()
    print(contents)
    contents_list = contents.split("\n")
    print(f"Number of names: {len(contents_list)}")