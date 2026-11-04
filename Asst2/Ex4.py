import time

import pandas as pd


def load_csv(filepath):
    print(f"Loading CSV file from: {filepath}")
    start_time = time.time()

    try:
        data = pd.read_csv(filepath, on_bad_lines="skip")
    except Exception as error:
        print("Error reading the CSV file:", error)
        return None

    load_time = time.time() - start_time
    print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
    print(f"Number of rows: {len(data)}")
    return data


def display_initial_rows(data):
    while True:
        response = input(
            "How many initial rows would you like to see? "
            "(enter a number, 'all', or press Enter to skip): "
        ).strip()

        if not response:
            print("Preview skipped.")
            return True

        if response.lower() == "all":
            preview = data.copy()
            preview.index = range(1, len(preview) + 1)
            preview.index.name = "Row"
            print(preview)
            return True

        try:
            number_of_rows = int(response)
            if number_of_rows < 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Enter a non-negative whole number, 'all', or press Enter to skip.")
            continue

        preview = data.head(number_of_rows).copy()
        preview.index = range(1, len(preview) + 1)
        preview.index.name = "Row"
        print(preview)
        return True


def show_employees_by_region(data):
    employees_by_region = data.groupby("sales_region")["employee_id"].nunique()
    print("\nNumber of employees by region:")
    print(employees_by_region)
    return True


def exit_program(data):
    print("Exiting the program.")
    return False


menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Show the number of employees by region", show_employees_by_region),
    ("Exit the program", exit_program),
)


def display_menu():
    print("\nSales Data Menu")
    for number, (description, _) in enumerate(menu_options, start=1):
        print(f"{number}. {description}")
    return input("Enter the number of your choice: ").strip()


def main():
    csv_file = (
        "https://drive.google.com/uc?export=download"
        "&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
    )
    sales_data = load_csv(csv_file)
    if sales_data is None:
        return

    running = True
    while running:
        selection = display_menu()

        if not selection.isdigit() or not 1 <= int(selection) <= len(menu_options):
            print(f"Invalid selection. Enter a number from 1 to {len(menu_options)}.")
            continue

        selected_description, selected_function = menu_options[int(selection) - 1]
        print(f"You selected: {selected_description}")
        running = selected_function(sales_data)


if __name__ == "__main__":
    main()