import csv
import os


PROJECT_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_FILE = os.path.join(
    PROJECT_FOLDER,
    "products.csv"
)


COLUMNS = [
    "name",
    "quantity",
    "unit_value",
    "subtotal"
]


def read_name(message):
    while True:
        name = input(message).strip()

        if name != "":
            return name

        print("The name cannot be empty.")


def read_quantity(message):
    while True:
        try:
            quantity = int(input(message))

            if quantity <= 0:
                print("Enter a quantity greater than zero.")
            else:
                return quantity

        except ValueError:
            print("Invalid entry. Enter an integer number.")


def read_value(message):
    while True:
        try:
            entry = input(message)
            entry = entry.replace(",", ".")

            value = float(entry)

            if value <= 0:
                print("Enter a value greater than zero.")
            else:
                return value

        except ValueError:
            print("Invalid entry. Enter numbers only.")


def create_product(name, quantity, unit_value):
    subtotal = quantity * unit_value

    product = {
        "name": name,
        "quantity": quantity,
        "unit_value": unit_value,
        "subtotal": subtotal
    }

    return product


def create_product_from_keyboard():
    print("\n=== PRODUCT REGISTRATION ===")

    name = read_name("Product name: ")
    quantity = read_quantity("Quantity: ")
    unit_value = read_value(
        "Unit value: R$ "
    )

    product = create_product(
        name,
        quantity,
        unit_value
    )

    return product


def save_products_csv(products):
    with open(
        CSV_FILE,
        mode="w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(products)

    print("Products saved successfully!")


def add_product_csv(product):
    with open(
        CSV_FILE,
        mode="a",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS,
            delimiter=";"
        )

        writer.writerow(product)

    print("New product added successfully!")


def read_products_csv():
    products = []

    with open(
        CSV_FILE,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";"
        )

        for row in reader:
            product = create_product(
                row["name"],
                int(row["quantity"]),
                float(row["unit_value"])
            )

            products.append(product)

    return products


def change_price_csv(searched_name):
    products = read_products_csv()

    for product in products:
        if product["name"].lower() == searched_name.lower():
            new_price = read_value(
                "Enter the new price: R$ "
            )

            product["unit_value"] = new_price
            product["subtotal"] = (
                product["quantity"] * new_price
            )

            save_products_csv(products)
            print("Price changed successfully!")
            return

    print("Product not found.")


def delete_product_csv(searched_name):
    products = read_products_csv()

    for product in products:
        if product["name"].lower() == searched_name.lower():
            products.remove(product)

            save_products_csv(products)
            print("Product deleted successfully!")
            return

    print("Product not found.")


def display_products():
    products = read_products_csv()
    total_general = 0

    print("\n=== REGISTERED PRODUCTS ===")

    if len(products) == 0:
        print("No products registered.")
        return

    for product in products:
        print(
            f"{product['name']} — "
            f"{product['quantity']} units — "
            f"R$ {product['unit_value']:.2f} each — "
            f"Subtotal: R$ {product['subtotal']:.2f}"
        )

        total_general += product["subtotal"]

    print(f"\nGeneral total: R$ {total_general:.2f}")


def move_inventory(searched_name, operation):
    products = read_products_csv()

    if operation not in ["e", "s"]:
        print("Invalid operation.")
        return

    for product in products:
        if product["name"].lower() == searched_name.lower():
            movement_quantity = read_quantity(
                "Enter the quantity: "
            )

            if operation == "e":
                product["quantity"] += movement_quantity
                message = "Entry registered successfully!"

            else:
                if movement_quantity > product["quantity"]:
                    print("Insufficient stock.")
                    return

                product["quantity"] -= movement_quantity
                message = "Exit registered successfully!"

            product["subtotal"] = (
                product["quantity"]
                * product["unit_value"]
            )

            save_products_csv(products)
            print(message)
            print(
                f"Current stock: "
                f"{product['quantity']} units"
            )
            return

    print("Product not found.")


def display_low_stock():
    products = read_products_csv()
    products_found = 0

    print("\n=== LOW STOCK ALERT ===")

    for product in products:
        if product["quantity"] <= 5:
            print(
                f"{product['name']} — "
                f"{product['quantity']} units remaining"
            )

            products_found += 1

    if products_found == 0:
        print("No products with low stock.")


# NEW FUNCTION:
# Creates the CSV only if it doesn't exist yet.
def initialize_file():
    if os.path.exists(CSV_FILE):
        print("Existing file loaded.")
        return

    initial_products = [
        create_product("Cake", 2, 50.0),
        create_product("Coffee", 3, 8.0)
    ]

    save_products_csv(initial_products)
    print("File created for the first time.")


def main():
    # UPDATED LINE:
    # No longer deletes the file on each run.
    initialize_file()

    new_product = create_product_from_keyboard()
    add_product_csv(new_product)

    name_to_change = read_name(
        "\nWhich product do you want to change? "
    )
    change_price_csv(name_to_change)

    name_to_delete = read_name(
        "\nWhich product do you want to delete? "
    )
    delete_product_csv(name_to_delete)

    display_products()


if __name__ == "__main__":
    main()
