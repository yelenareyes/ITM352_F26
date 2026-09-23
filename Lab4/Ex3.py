# manipulate a list in various tricky ways
# Name: Yelena Reyes
# Date: Sept. 16, 2026

response_values = [5, 7, 3, 8]
response_values.append(0)
print("Response values after appending 0:", response_values)
response_values.insert(2, 6)
response_values = response_values[:2] + [6] + response_values[2:]
print("Response values after inserting 6 at index 2:", response_values)

# Name: Yelena Reyes
# Date: Sept. 18, 2026

url = input("Enter a URL: https://shidler.hawaii.edu/")

cleaned_url = url.replace("https://", "")
cleaned_url = cleaned_url.replace("/", "")
print("Cleaned URL:", cleaned_url)

parts = cleaned_url.split(".")
print("The parts are: ", parts)

domain_name = parts[1]
TLD = parts[2]
print("Domain name:", domain_name)
print("TLD:", TLD)
