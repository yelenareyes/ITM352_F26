import time
from datetime import datetime

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
    """Ask how many initial rows to display, or let the user skip."""
    print(f"\nThere are {len(data)} rows available.")

    while True:
        response = input(
            "\nEnter rows to display:\n"
            f"- Enter a number 1 to {len(data)}\n"
            "- To see all rows, enter 'all'\n"
            "- To skip preview, press Enter\n\n"
            "Your choice: "
        ).strip().lower()

        if not response:
            print("Skipping data preview.")
            return None
        if response == "all":
            print(data.to_string())
            return data

        try:
            number_of_rows = int(response)
        except ValueError:
            print("Invalid input. Enter a whole number or 'all'.")
            continue

        if not 1 <= number_of_rows <= len(data):
            print(f"Please enter a number from 1 to {len(data)}.")
            continue

        result = data.head(number_of_rows)
        print(result)
        return result


def filter_sales_by_date_range(data):
    """Prompt for inclusive dates and return only sales within that range."""
    if "order_date" not in data.columns:
        print("Cannot filter sales: the data has no 'order_date' column.")
        return None

    while True:
        start_input = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_input = input("Enter the end date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(start_input, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Enter dates using YYYY-MM-DD, for example 2019-02-01.")
            continue

        if start_date > end_date:
            print("The start date must be on or before the end date.")
            continue
        break

    order_dates = pd.to_datetime(
        data["order_date"], format="%m/%d/%Y", errors="coerce"
    )
    unparsed = order_dates.isna()
    for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
        order_dates.loc[unparsed] = pd.to_datetime(
            data.loc[unparsed, "order_date"],
            format=date_format,
            errors="coerce",
        )
        unparsed = order_dates.isna()

    if unparsed.any():
        print(f"Skipping {int(unparsed.sum())} rows with unrecognized order dates.")

    in_range = (
        order_dates.notna()
        & (order_dates >= pd.Timestamp(start_date))
        & (order_dates <= pd.Timestamp(end_date))
    )
    filtered_data = data.loc[in_range]
    if filtered_data.empty:
        print("No sales were found in that date range; analysis skipped.")
    else:
        print(
            f"Analyzing {len(filtered_data)} sales from "
            f"{start_date} through {end_date}."
        )
    return filtered_data


def get_user_selection(options, prompt, required=False, single=False):
    """Return user-selected options by their displayed number."""
    while True:
        print(prompt)
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")

        choice = input("Enter number(s), separated by commas: ").strip()
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []

        try:
            indexes = [int(value.strip()) for value in choice.split(",")]
        except ValueError:
            print("Invalid input. Enter numbers separated by commas.")
            continue

        if any(index < 1 or index > len(options) for index in indexes):
            print(f"Each number must be between 1 and {len(options)}.")
            continue

        selected = list(dict.fromkeys(options[index - 1] for index in indexes))
        if single and len(selected) != 1:
            print("Please select exactly one option.")
            continue
        return selected


def create_sales_column(data):
    """Return a copy of the sales data with a calculated sales column."""
    required = ["quantity", "unit_price"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None
    return data.assign(sales=data["quantity"] * data["unit_price"])


def show_total_sales_by_region_and_order_type(data):
    """Display total sales by region and order type."""
    required = ["sales_region", "order_type"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    sales = create_sales_column(data)
    if sales is None:
        return None
    result = pd.pivot_table(
        sales,
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    ).round(2)
    print("\nTotal sales by region and order type:")
    print(result)
    return result


def show_average_sales_by_region(data):
    """Display average sales by region, state, and order type."""
    required = ["sales_region", "customer_state", "order_type"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    sales = create_sales_column(data)
    if sales is None:
        return None
    result = pd.pivot_table(
        sales,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
    ).round(2)
    print("\nAverage sales by region, state, and order type:")
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(result)
    return result


def show_sales_by_customer_type_and_order_type_by_state(data):
    """Display total sales by customer type and order type, by state."""
    required = ["customer_type", "customer_state", "order_type"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    sales = create_sales_column(data)
    if sales is None:
        return None
    result = pd.pivot_table(
        sales,
        index=["customer_type", "order_type"],
        columns="customer_state",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    ).round(2)
    print("\nTotal sales by customer type and order type, by state:")
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(result)
    return result


def show_total_sales_quantity_and_price_by_region_and_product(data):
    """Display total quantity and sales by region and product."""
    required = ["sales_region", "produce_name", "quantity", "unit_price"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    sales = create_sales_column(data)
    if sales is None:
        return None
    result = pd.pivot_table(
        sales,
        index="sales_region",
        columns="produce_name",
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    ).round(2)
    print("\nTotal sales quantity and price by region and product:")
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(result)
    return result


def show_total_sales_quantity_and_price_by_customer_type(data):
    """Display total quantity and sales by order and customer type."""
    required = ["order_type", "customer_type", "quantity", "unit_price"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    sales = create_sales_column(data)
    if sales is None:
        return None
    result = pd.pivot_table(
        sales,
        index="order_type",
        columns="customer_type",
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    ).round(2)
    print("\nTotal sales quantity and sales by customer type:")
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(result)
    return result


def show_max_min_sales_price_by_category(data):
    """Display maximum and minimum unit price for each product category."""
    required = ["product_category", "unit_price"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    result = data.groupby("product_category")["unit_price"].agg(
        maximum="max", minimum="min"
    ).round(2)
    print("\nMaximum and minimum sales price by category:")
    print(result.to_string())
    return result


def show_employees_by_region(data):
    """Display the number of unique employees in each sales region."""
    required = ["sales_region", "employee_id"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return None

    result = data.groupby("sales_region")["employee_id"].nunique()
    print("\nNumber of unique employees by region:")
    print(result.to_string())
    return result


def generate_custom_pivot_table(data):
    """Interactively build and display a custom pivot table."""
    row_options = list(data.columns)
    rows = get_user_selection(
        row_options, "\nSelect row field(s) (required):", required=True
    )
    column_options = [column for column in row_options if column not in rows]
    columns = get_user_selection(
        column_options, "\nSelect column field(s) (optional; Enter to skip):"
    )

    value_options = list(data.select_dtypes(include="number").columns)
    if not value_options:
        print("No numeric columns are available to aggregate.")
        return None
    values = get_user_selection(
        value_options, "\nSelect a value to aggregate:", required=True, single=True
    )[0]
    aggregations = ["sum", "mean", "count"]
    aggregation = get_user_selection(
        aggregations, "\nSelect an aggregation:", required=True, single=True
    )[0]

    try:
        result = pd.pivot_table(
            data,
            index=rows,
            columns=columns if columns else None,
            values=values,
            aggfunc=aggregation,
        )
    except (KeyError, ValueError, TypeError) as error:
        print("Could not create the pivot table:", error)
        return None

    print("\nCustom pivot table:")
    print(result)
    return result


def export_result_to_excel(result):
    """Ask whether to export a result and save it as an Excel workbook."""
    while True:
        response = input(
            "\nWould you like to export this result to Excel? (y/n): "
        ).strip().lower()
        if response in ("y", "yes"):
            break
        if response in ("n", "no"):
            return
        print("Please enter y or n.")

    filename = input("Enter a filename for the Excel file: ").strip()
    if not filename:
        print("Export cancelled: a filename is required.")
        return
    if not filename.lower().endswith(".xlsx"):
        filename += ".xlsx"

    try:
        result.to_excel(filename, sheet_name="Results")
    except (ImportError, OSError, ValueError) as error:
        print(f"Error exporting results to Excel: {error}")
        return
    print(f"Results exported to {filename}")


def exit_program(data):
    """End the dashboard loop."""
    print("Exiting the program. Goodbye!")
    return False


menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Total sales by region and order_type", show_total_sales_by_region_and_order_type),
    (
        "Average sales by region with average sales by state and sale type",
        show_average_sales_by_region,
    ),
    (
        "Sales by customer type and order type by state",
        show_sales_by_customer_type_and_order_type_by_state,
    ),
    (
        "Total sales quantity and price by region and product",
        show_total_sales_quantity_and_price_by_region_and_product,
    ),
    (
        "Total sales quantity and price by customer type",
        show_total_sales_quantity_and_price_by_customer_type,
    ),
    ("Max and min sales price of sales by category", show_max_min_sales_price_by_category),
    ("Number of unique employees by region", show_employees_by_region),
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Exit", exit_program),
)


def display_menu():
    """Display the dashboard menu and return the selected option index."""
    while True:
        print("\n--- Sales Data Dashboard ---")
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"{number}. {description}")

        choice = input(f"Select an option (1-{len(menu_options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection. Enter a number from 1 to {len(menu_options)}.")


def main():
    csv_file = (
        "https://drive.google.com/uc?export=download"
        "&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
    )
    sales_data = load_csv(csv_file)
    if sales_data is None:
        return

    try:
        running = True
        while running:
            selection = display_menu()
            _, action = menu_options[selection]

            if action is display_initial_rows:
                result = action(sales_data)
            elif action is exit_program:
                running = action(sales_data)
                continue
            else:
                analysis_data = filter_sales_by_date_range(sales_data)
                if analysis_data is None or analysis_data.empty:
                    continue
                result = action(analysis_data)

            if result is not None:
                export_result_to_excel(result)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")


if __name__ == "__main__":
    main()

menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Average sales by region with average sales by state and sale type", show_average_sales_by_region),
    ("Total sales by region and order type", show_total_sales_by_region_and_order_type),
    ("Sales by customer type and order type by state.", show_sales_by_customer_type_and_order_type_by_state),
    ("Total sales quantity and price by region and product",show_total_sales_quantity_and_price_by_region_and_product),
    ("Total sales quantity and price by customer type", show_total_sales_quantity_and_price_by_customer_type),
    ("Max and min sales price of sales by category", show_max_min_sales_price_by_category),
    ("Number of unique employees by region", show_employees_by_region),
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Exit the program", exit_program),


)


def display_menu():
    """Show the menu and return a valid selection as an index into menu_options."""
    while True:
        print("\nSales Data Menu")
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"  {number}. {description}")

        choice = input(f"Select an option (1-{len(menu_options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection '{choice}'. Please enter a number from 1 to {len(menu_options)}.")


def main():
    csv_file = 'https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K&export=download'
    # csv_file = "junk.csv"  # Intentionally incorrect path to test error handling
    sales_data = load_csv(csv_file)

    if sales_data is None:
        return

    try:
        while True:
            selection = display_menu()
            _, action = menu_options[selection]
            if action in (display_initial_rows, exit_program):
                action_data = sales_data
            else:
                action_data = filter_sales_by_date_range(sales_data)
                if action_data is None or action_data.empty:
                    continue

            result = action(action_data)
            if result is not None:
                export_result_to_excel(result)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")


if __name__ == "__main__":
    main()