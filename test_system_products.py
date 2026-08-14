import os
import tempfile
import unittest
from unittest.mock import patch

import system_products as inventory


class TestSystemProducts(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.test_csv = os.path.join(
            self.temp_directory.name,
            "test_products.csv"
        )

        self.csv_patch = patch.object(
            inventory,
            "CSV_FILE",
            self.test_csv
        )

        self.csv_patch.start()

        initial_products = [
            inventory.create_product("Cake", 2, 50.0),
            inventory.create_product("Coffee", 3, 8.0)
        ]

        with patch("builtins.print"):
            inventory.save_products_csv(initial_products)

    def tearDown(self):
        self.csv_patch.stop()
        self.temp_directory.cleanup()

    def test_create_product_calculates_subtotal(self):
        product = inventory.create_product(
            "Milk",
            4,
            6.5
        )

        self.assertEqual(product["name"], "Milk")
        self.assertEqual(product["quantity"], 4)
        self.assertEqual(product["unit_value"], 6.5)
        self.assertEqual(product["subtotal"], 26.0)

    def test_read_products_from_csv(self):
        products = inventory.read_products_csv()

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]["name"], "Cake")
        self.assertEqual(products[1]["name"], "Coffee")

    def test_add_product(self):
        milk = inventory.create_product(
            "Milk",
            5,
            6.0
        )

        with patch("builtins.print"):
            inventory.add_product_csv(milk)

        products = inventory.read_products_csv()

        self.assertEqual(len(products), 3)
        self.assertEqual(products[2]["name"], "Milk")

    def test_change_product_price(self):
        with patch.object(
            inventory,
            "read_value",
            return_value=60.0
        ):
            with patch("builtins.print"):
                inventory.change_price_csv("cake")

        products = inventory.read_products_csv()
        cake = products[0]

        self.assertEqual(cake["unit_value"], 60.0)
        self.assertEqual(cake["subtotal"], 120.0)

    def test_delete_product(self):
        with patch("builtins.print"):
            inventory.delete_product_csv("coffee")

        products = inventory.read_products_csv()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Cake")

    def test_stock_entry(self):
        with patch.object(
            inventory,
            "read_quantity",
            return_value=3
        ):
            with patch("builtins.print"):
                inventory.move_inventory("cake", "e")

        products = inventory.read_products_csv()
        cake = products[0]

        self.assertEqual(cake["quantity"], 5)
        self.assertEqual(cake["subtotal"], 250.0)

    def test_stock_exit(self):
        with patch.object(
            inventory,
            "read_quantity",
            return_value=1
        ):
            with patch("builtins.print"):
                inventory.move_inventory("cake", "s")

        products = inventory.read_products_csv()
        cake = products[0]

        self.assertEqual(cake["quantity"], 1)
        self.assertEqual(cake["subtotal"], 50.0)

    def test_insufficient_stock_does_not_change_quantity(self):
        with patch.object(
            inventory,
            "read_quantity",
            return_value=10
        ):
            with patch("builtins.print"):
                inventory.move_inventory("cake", "s")

        products = inventory.read_products_csv()
        cake = products[0]

        self.assertEqual(cake["quantity"], 2)


if __name__ == "__main__":
    unittest.main()