import pandas as pd
import time


def load_csv(filepath):
    print(f"Loading CSV file from: {filepath}")
    start_time = time.time()

    try:
        df = pd.read_csv(filepath, on_bad_lines="skip")
        load_time = time.time() - start_time
        print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
        print(f"Number of rows: {len(df)}")
        return df

    except Exception as e:
        print("Error reading the CSV file:", e)
        return None


def display_initial_rows(data):
    while True:
        rows_to_display = input(
            "How many initial rows would you like to see? "
            "(enter a number, 'all', or press Enter to skip): "
        ).strip()

        if not rows_to_display:
            print("Preview skipped.")
            return

        if rows_to_display.lower() == "all":
            print(data)
            return

        if num_rows < 1:
            print(f"Only {len(data)} rows available; showing all of them.")
            continue

        try:
            number_of_rows = int(rows_to_display)
            if number_of_rows < 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Enter a non-negative whole number, 'all', or press Enter to skip.")
            continue

        print(data.head(number_of_rows))
        return


csv_file = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
sales_data = load_csv(csv_file)

if sales_data is not None:
    display_initial_rows(sales_data)
    print("\nData types of the dataframe fields:")
    print(sales_data.dtypes)

