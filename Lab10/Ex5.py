# Import homes data and create a dataframe
import pandas as pd

homes_data_file = "https://drive.google.com/uc?id=1M-X_bypJJ6K5p6eM6aYBwt1qIizIiIex"
home_df = pd.read_csv(homes_data_file)
print(home_df.head())

# Print the dimensions of the dataframe
shape = home_df.shape
print("The dimensions of the dataframe are:", shape)


df_big = home_df[home_df['units'] >= 500]
print(df_big.head(10))
print("The dimensions of the filtered dataframe are:", df_big.shape)
