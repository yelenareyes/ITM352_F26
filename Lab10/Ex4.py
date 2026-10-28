# Read a json file of taxi trip data and create a dataframe and some simple stats
import pandas as pd

df = pd.read_json("Taxi_Trips.json")
print(df)

summary = df.describe()  # Get summary statistics for the dataframe
print(summary)  # Print the summary statistics

# Read the JSON file into a DataFrame
results_df = pd.read_json("Taxi_Trips.json")
print(results_df.head(6))

# Display basic statistics about the DataFrame
print(results_df.describe())

median = results_df.median()
print("The median fare value is:", median)



