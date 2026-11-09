import contextlib
import io
import unittest
from unittest.mock import patch

import pandas as pd

import V4


def sample_sales():
    return pd.DataFrame(
        {
            "sales_region": ["North", "North", "South", "South"],
            "customer_state": ["HI", "HI", "CA", "CA"],
            "order_type": ["Retail", "Wholesale", "Retail", "Retail"],
            "customer_type": ["Individual", "Business", "Individual", "Business"],
            "quantity": [2, 1, 3, 2],
            "unit_price": [10.0, 20.0, 5.0, 7.5],
            "product_category": ["Oil", "Gift", "Oil", "Gift"],
            "employee_id": [101, 102, 101, 103],
            "produce_name": ["Oil A", "Gift A", "Oil A", "Gift B"],
            "order_date": ["01/15/2020", "20/02/2020", "2020-03-03", "bad-date"],
        }
    )


class DashboardTests(unittest.TestCase):
    def test_load_csv_success(self):
        data = sample_sales()
        with patch.object(V4.pd, "read_csv", return_value=data):
            self.assertIs(V4.load_csv("sales.csv"), data)

    def test_load_csv_reports_read_error(self):
        with patch.object(V4.pd, "read_csv", side_effect=OSError("unavailable")):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertIsNone(V4.load_csv("missing.csv"))

    def test_missing_columns_helper(self):
        self.assertEqual(
            V4.missing_columns(sample_sales(), ["sales_region", "missing"]),
            ["missing"],
        )

    def test_prepare_sales_data_computes_amount_and_handles_bad_numbers(self):
        data = sample_sales()
        data.loc[0, "quantity"] = "bad"
        with contextlib.redirect_stdout(io.StringIO()):
            prepared = V4.prepare_sales_data(data)
        self.assertTrue(pd.isna(prepared.loc[0, "sales"]))
        self.assertEqual(prepared.loc[1, "sales"], 20.0)
        self.assertEqual(data.loc[0, "quantity"], "bad")

    def test_prepare_sales_data_requires_columns(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(V4.prepare_sales_data(pd.DataFrame({"quantity": [1]})))

    def test_display_initial_rows_number_all_skip_and_invalid(self):
        data = sample_sales()
        for responses, expected in ((["2"], 2), (["all"], 4), ([""], None),
                                    (["invalid", "0", "2"], 2)):
            output = io.StringIO()
            with patch("builtins.input", side_effect=responses):
                with contextlib.redirect_stdout(output):
                    result = V4.display_initial_rows(data)
            if expected is None:
                self.assertIsNone(result)
            else:
                self.assertEqual(len(result), expected)
            self.assertIn("4 rows available", output.getvalue())

    def test_filter_sales_by_date_range_is_inclusive(self):
        with patch("builtins.input", side_effect=["2020-01-15", "2020-02-20"]):
            with contextlib.redirect_stdout(io.StringIO()):
                result = V4.filter_sales_by_date_range(sample_sales())
        self.assertEqual(result.index.tolist(), [0, 1])

    def test_filter_sales_retries_invalid_range_and_handles_missing_column(self):
        inputs = ["bad", "2020-02-20", "2020-01-01", "2020-03-01"]
        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(io.StringIO()):
                result = V4.filter_sales_by_date_range(sample_sales())
        self.assertEqual(result.index.tolist(), [0, 1, 2])
        with contextlib.redirect_stdout(io.StringIO()):
            missing = V4.filter_sales_by_date_range(pd.DataFrame({"sales": [1]}))
        self.assertIsNone(missing)

    def test_employee_counts_and_missing_columns(self):
        with contextlib.redirect_stdout(io.StringIO()):
            counts = V4.show_employees_by_region(sample_sales())
            missing = V4.show_employees_by_region(pd.DataFrame({"sales_region": []}))
        self.assertEqual(counts.to_dict(), {"North": 2, "South": 2})
        self.assertIsNone(missing)

    def test_get_user_selection_validates_and_deduplicates(self):
        with patch("builtins.input", side_effect=["bad", "1, 1, 2"]):
            with contextlib.redirect_stdout(io.StringIO()):
                selected = V4.get_user_selection(["a", "b"], "Select")
        self.assertEqual(selected, ["a", "b"])
        with patch("builtins.input", return_value=""):
            self.assertEqual(V4.get_user_selection([], "Select"), [])

    def test_generate_custom_pivot_table(self):
        with patch("builtins.input", side_effect=["1", "", "1", "1"]):
            with contextlib.redirect_stdout(io.StringIO()):
                result = V4.generate_custom_pivot_table(sample_sales())
        self.assertEqual(result.loc["North"], 3)
        self.assertEqual(result.loc["South"], 5)

    def test_predefined_analyses_return_expected_tables(self):
        data = sample_sales()
        with contextlib.redirect_stdout(io.StringIO()):
            total = V4.show_total_sales_by_region_and_order_type(data)
            average = V4.show_average_sales_by_region(data)
            state_sales = V4.show_sales_by_customer_type_and_order_type_by_state(data)
            product_sales = V4.show_total_sales_quantity_and_price_by_region_and_product(data)
            customer_sales = V4.show_total_sales_quantity_and_price_by_customer_type(data)
            category_prices = V4.show_max_min_sales_price_by_category(data)

        self.assertEqual(total.loc["North", "Retail"], 20.0)
        self.assertEqual(average.loc["North", ("HI", "Retail")], 20.0)
        self.assertEqual(state_sales.loc[("Individual", "Retail"), "HI"], 20.0)
        self.assertEqual(product_sales.loc["North", ("sales", "Oil A")], 20.0)
        self.assertEqual(customer_sales.loc["Retail", ("quantity", "Individual")], 5)
        self.assertEqual(category_prices.loc["Oil", "maximum"], 10.0)

    def test_predefined_analyses_report_missing_columns(self):
        incomplete = pd.DataFrame({"sales_region": ["North"]})
        actions = (
            V4.show_total_sales_by_region_and_order_type,
            V4.show_average_sales_by_region,
            V4.show_sales_by_customer_type_and_order_type_by_state,
            V4.show_total_sales_quantity_and_price_by_region_and_product,
            V4.show_total_sales_quantity_and_price_by_customer_type,
            V4.show_max_min_sales_price_by_category,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            for action in actions:
                self.assertIsNone(action(incomplete))

    def test_export_result_prompts_and_adds_extension(self):
        result = pd.DataFrame({"sales": [1]})
        with patch("builtins.input", side_effect=["maybe", "yes", "report"]), \
             patch.object(pd.DataFrame, "to_excel") as to_excel:
            with contextlib.redirect_stdout(io.StringIO()):
                V4.export_result_to_excel(result)
        to_excel.assert_called_once_with("report.xlsx", sheet_name="Results")

    def test_export_result_can_be_skipped(self):
        with patch("builtins.input", return_value="no"), \
             patch.object(pd.DataFrame, "to_excel") as to_excel:
            V4.export_result_to_excel(pd.DataFrame({"sales": [1]}))
        to_excel.assert_not_called()

    def test_exit_program_exits(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                V4.exit_program()

    def test_menu_contains_ten_callable_actions_and_validates_choice(self):
        self.assertEqual(len(V4.menu_options), 10)
        self.assertTrue(all(callable(action) for _, action in V4.menu_options))
        with patch("builtins.input", side_effect=["0", "2"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(V4.display_menu(), 1)

    def test_main_dispatches_exit_action(self):
        with patch.object(V4, "load_csv", return_value=sample_sales()), \
             patch.object(V4, "display_menu", return_value=9):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    V4.main()


if __name__ == "__main__":
    unittest.main()
