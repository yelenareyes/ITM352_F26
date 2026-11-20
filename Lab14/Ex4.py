# Get public licence data from City of Chicago's data portal
import pandas as pd
from sodapy import Socrata

# Replace 'YOUR_APP_TOKEN' with your actual Socrata application token
client = Socrata("data.cityofchicago.org", "YOUR_APP_TOKEN")

# Specify the specific JSON file
json_file ="rr23-ymwb"

results = client.get(json_file, limit=500)
# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.head()

vehicles = results_df[["public_vehicle_number", "vehicle_fuel_source"]]
print("Public Vehicle Number and Fuel Source:")

vehicles.info()