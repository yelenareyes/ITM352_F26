
from time import time

import pandas as pd
import ssl

# Tell pandas to print all columns when displaying a DataFrame
pd.set_option('display.max_columns', None)

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context

csv_file = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
outfile = "sales_data_test.csv"

try:
    df = pd.read_csv(csv_file, engine='pyarrow', on_bad_lines='skip')
    end_time = time.time()
    print(f"Time taken to load the data: {end_time - start_time} seconds")

    df.head(10).to_csv(outfile, index=False)
    print(f"First 10 rows of {csv_file} saved to {outfile}")
    print(df.head())

    # Calculate sales total per row, for later use in the pivot table
    df['sales'] = df['quantity'] * df['unit_price']

    # Create a pivot table aggregating sales by region and order_type
    pivot_table = pd.pivot_table(
        df,
        values='sales',
        index='region',
        columns='order_type',
        aggfunc=np.sum,
        margins=True,
        margins_name='Total Sales'
    )

    print(pivot_table)

except Exception as e:
    print("Error while loading or processing the sales data:", e)

# Call load_csv to load the data and print the first 10 rows 
csv_file ='https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=sharing'
