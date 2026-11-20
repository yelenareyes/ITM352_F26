# Get a JSON file from City of Chicago's data portal and analyze driver types
import pandas as pd
import requests

url = "https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type"
response = requests.get(url)

print("Driver Type Counts:")
print(response.json())

response_df = pd.DataFrame.from_records(response.json())
# Ensure the DataFrame has the expected columns before renaming and setting index
if 'driver_type' in response_df.columns and 'count_license' in response_df.columns:
	response_df = response_df.rename(columns={'count_license': 'count'})
	response_df = response_df.set_index('driver_type')
else:
	print("Unexpected columns in API response:", response_df.columns)

print(response_df)
