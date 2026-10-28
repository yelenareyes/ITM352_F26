import pandas as pd

csv_file = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

try:
    df = pd.read_csv(csv_file, engine='python', on_bad_lines='skip')
    print(df.head())
except Exception as e:
    print("Error reading the CSV file:", e)


