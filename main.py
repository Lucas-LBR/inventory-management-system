from system_products import (
    initialize_file,
    create_product_from_keyboard,
    add_product_csv,
    display_products,
    change_price_csv,
    delete_product_csv,
    display_low_stock,
    move_inventory,
    read_name
)


def show_menu():
    print("\n=== INVENTORY SYSTEM ===")
    print("1 - Register product")
    print("2 - List products")
    print("3 - Change price")
    print("4 - Delete product")
    print("5 - View low stock")
    print("6 - Register entry or exit")
    print("7 - Exit")

    return input("\nChoose an option: ").strip()


def main():
    initialize_file()

    while True:
        option = show_menu()

        if option == "1":
            product = create_product_from_keyboard()
            add_product_csv(product)

        elif option == "2":
            display_products()

        elif option == "3":
            name = read_name(
                "\nWhich product do you want to change? "
            )
            change_price_csv(name)

        elif option == "4":
            name = read_name(
                "\nWhich product do you want to delete? "
            )

            confirmation = input(
                f"Confirm deletion of '{name}'? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                delete_product_csv(name)
            else:
                print("Deletion cancelled.")

        elif option == "5":
            display_low_stock()

        elif option == "6":
            name = read_name(
                "\nWhich product do you want to move? "
            )

            operation = input(
                "Type E for entry or S for exit: "
            ).strip().lower()

            move_inventory(
                name,
                operation
            )

        elif option == "7":
            print("Program ended.")
            break

        else:
            print("Invalid option. Choose from 1 to 7.")


if __name__ == "__main__":
    main()
    