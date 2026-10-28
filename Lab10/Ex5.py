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

df_big = home_df[home_df['units'] >= 500]
df_big= df_big.drop(columns=['easement'])
print(df_big.head(10))

# Look at the data types 
print(home_df.dtypes)

# Coerce_land_sqft, gross_sqft, and sale_price to numeric
df_big['land_sqft'] = pd.to_numeric(df_big['land_sqft'], errors='coerce')
df_big['gross_sqft'] = pd.to_numeric(df_big['gross_sqft'], errors='coerce')
df_big['sale_price'] = pd.to_numeric(df_big['sale_price'], errors='coerce')

# Look at the data types and print the cleaned data
print("After cleaning...")
print(df_big.dtypes)
print(df_big.head(10))

# We have some null values. Drop these.
df_big = df_big.dropna()

# Now drop duplicate records.
df_big = df_big.drop_duplicates()
print("After dropping duplicate records...")
print(df_big.info())
print(df_big.head(10))


# Filter out 0 sales
df_big = df_big[df_big['sale_price'] > 0]
print("After filtering out 0 sales...")
print(df_big.info())
print(df_big.head(10))