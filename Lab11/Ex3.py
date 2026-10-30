# Create a dataframe from a CSV file and create a pivot table aggregating sales by region and order_type.

import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate errors
ssl_create_default_https_context = ssl._create_unverified_context
# Tell pandas to print all columns when displaying a DatFrame
pd.set_option('display.max_columns', None)

csv_file = "https://drive.google.com/file/d/1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K/view"

try:
    df = pd.read_csv(csv_file, engine='python', on_bad_lines='skip')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='%Y-%m-%d')
    print(df.head())

    # Calculate sales total per row, for later use in the pivot table
    df['sales'] = df['quantity'] * df['unit_price']

    # Create a pivot table aggregating sales by region and order_type
    pivot_table = pd.pivot_table(df,
                             values='sales', 
                             index='customer_state', 
                             columns='order_type', 
                             aggfunc='mean', 
                             margins_name = 'Total Sales')

    print(pivot_table)
    
except Exception as e:
    print("Error occurred while reading the CSV file:", e)
