
resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3},
]

fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []


def find_resource(resource_id):
    for resource in resources:
        if resource["id"].casefold() == resource_id.strip().casefold():
            return resource
    return None


def list_resources():
    print("\n--- RESOURCE INVENTORY ---")
    for resource in resources:
        borrowed = resource["total"] - resource["available"]
        print(
            f'{resource["id"]} | {resource["name"]} | '
            f'{resource["category"]} | Total: {resource["total"]} | '
            f'Available: {resource["available"]} | Borrowed: {borrowed}'
        )


def add_resource(resource_id, name, category, total):
    resource_id = resource_id.strip()
    name = name.strip()
    category = category.strip()

    if not resource_id or not name or not category:
        print("Error: ID, name and category cannot be empty.")
        return

    if find_resource(resource_id):
        print("Error: That resource ID already exists.")
        return

    if not isinstance(total, int) or isinstance(total, bool) or total <= 0:
        print("Error: Total units must be a positive integer.")
        return

    resources.append({
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    })
    print(f"Added {name} successfully.")


def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource = find_resource(resource_id)

    if fellow_id not in fellows:
        print("Borrowing rejected: Fellow ID not found.")
        return False

    if resource is None:
        print("Borrowing rejected: Resource ID not found.")
        return False

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        print("Borrowing rejected: Quantity must be a positive integer.")
        return False

    if quantity > resource["available"]:
        print(
            f'Borrowing rejected: Only {resource["available"]} '
            f'{resource["name"]}(s) available.'
        )
        return False

    resource["available"] -= quantity

    borrow_records.append({
        "fellow_id": fellow_id,
        "resource_id": resource["id"],
        "quantity": quantity,
        "outstanding": quantity
    })

    print(
        f'{fellows[fellow_id]} borrowed {quantity} '
        f'{resource["name"]}(s) successfully.'
    )
    return True


def return_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource = find_resource(resource_id)

    if fellow_id not in fellows:
        print("Return rejected: Fellow ID not found.")
        return False

    if resource is None:
        print("Return rejected: Resource ID not found.")
        return False

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        print("Return rejected: Quantity must be a positive integer.")
        return False

    outstanding = sum(
        record["outstanding"]
        for record in borrow_records
        if record["fellow_id"] == fellow_id
        and record["resource_id"] == resource["id"]
    )

    if quantity > outstanding:
        print(
            f'Return rejected: {fellows[fellow_id]} has only '
            f'{outstanding} outstanding {resource["name"]}(s).'
        )
        return False

    remaining = quantity

    for record in borrow_records:
        if (
            record["fellow_id"] == fellow_id
            and record["resource_id"] == resource["id"]
            and record["outstanding"] > 0
        ):
            returned = min(record["outstanding"], remaining)
            record["outstanding"] -= returned
            remaining -= returned

            if remaining == 0:
                break

    resource["available"] += quantity

    print(
        f'{fellows[fellow_id]} returned {quantity} '
        f'{resource["name"]}(s) successfully.'
    )
    return True


def search_resources(name):
    query = name.strip().casefold()
    matches = [
        resource for resource in resources
        if query in resource["name"].casefold()
    ]

    print(f'\n--- SEARCH RESULTS: "{name}" ---')

    if not matches:
        print("No matching resources found.")

    for resource in matches:
        print(
            f'{resource["id"]} | {resource["name"]} | '
            f'{resource["category"]} | Available: {resource["available"]}'
        )

    return matches


def filter_by_category(category):
    query = category.strip().casefold()
    matches = [
        resource for resource in resources
        if resource["category"].casefold() == query
    ]

    print(f"\n--- CATEGORY: {category} ---")

    if not matches:
        print("No resources found in this category.")

    for resource in matches:
        print(
            f'{resource["id"]} | {resource["name"]} | '
            f'Available: {resource["available"]}/{resource["total"]}'
        )

    return matches


def generate_report():
    total_units = sum(resource["total"] for resource in resources)
    available_units = sum(resource["available"] for resource in resources)
    borrowed_units = total_units - available_units

    low_stock = [
        resource for resource in resources
        if resource["available"] < 3
    ]

    borrowed_per_resource = {
        resource["id"]: resource["total"] - resource["available"]
        for resource in resources
    }

    most_borrowed = max(borrowed_per_resource.values(), default=0)

    leaders = [
        resource for resource in resources
        if most_borrowed > 0
        and borrowed_per_resource[resource["id"]] == most_borrowed
    ]

    print("\n========== INVENTORY REPORT ==========")
    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Units currently borrowed: {borrowed_units}")

    print("\nResources with fewer than 3 available units:")

    if low_stock:
        for resource in low_stock:
            print(
                f'  {resource["name"]}: '
                f'{resource["available"]} available'
            )
    else:
        print("  None")

    print("\nResource(s) with the most units currently borrowed:")

    if leaders:
        for resource in leaders:
            print(
                f'  {resource["name"]}: '
                f'{borrowed_per_resource[resource["id"]]} borrowed'
            )
    else:
        print("  None; no units are currently borrowed.")

    print("======================================")

    return {
        "total_units": total_units,
        "available_units": available_units,
        "borrowed_units": borrowed_units,
        "low_stock": low_stock,
        "most_borrowed": leaders
    }


def read_positive_integer(prompt):
    try:
        value = int(input(prompt).strip())
        if value <= 0:
            print("Error: Enter a number greater than zero.")
            return None
        return value
    except ValueError:
        print("Error: Enter a valid whole number.")
        return None


def run_demonstration():
    print("\n========== REQUIRED DEMONSTRATION ==========")

    print("\n1. F001 borrows 2 laptops")
    borrow_resource("F001", "R001", 2)
    print("Laptop available:", find_resource("R001")["available"])

    print("\n2. F002 borrows 3 keyboards")
    borrow_resource("F002", "R002", 3)
    print("Keyboard available:", find_resource("R002")["available"])

    print("\n3. F001 returns 1 laptop")
    return_resource("F001", "R001", 1)
    print("Laptop available:", find_resource("R001")["available"])

    print("\n4. F003 requests 4 headsets")
    borrow_resource("F003", "R003", 4)
    print("Headset available:", find_resource("R003")["available"])

    print("\n5. F002 tries to return 4 keyboards")
    return_resource("F002", "R002", 4)
    print("Keyboard available:", find_resource("R002")["available"])

    print("\n6. Search for LAPtop")
    search_resources("LAPtop")

    print("\n7. Generate report")
    generate_report()


def main():
    run_demonstration()

    while True:
        print("""
========== RESOURCE INVENTORY MENU ==========
1. List resources
2. Add resource
3. Borrow resource
4. Return resource
5. Search by name
6. Filter by category
7. Generate report
8. Exit
""")

        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            list_resources()

        elif choice == "2":
            resource_id = input("Resource ID: ")
            name = input("Resource name: ")
            category = input("Category: ")
            total = read_positive_integer("Total units: ")

            if total is not None:
                add_resource(resource_id, name, category, total)

        elif choice == "3":
            fellow_id = input("Fellow ID: ")
            resource_id = input("Resource ID: ")
            quantity = read_positive_integer("Quantity to borrow: ")

            if quantity is not None:
                borrow_resource(fellow_id, resource_id, quantity)

        elif choice == "4":
            fellow_id = input("Fellow ID: ")
            resource_id = input("Resource ID: ")
            quantity = read_positive_integer("Quantity to return: ")

            if quantity is not None:
                return_resource(fellow_id, resource_id, quantity)

        elif choice == "5":
            search_resources(input("Enter resource name: "))

        elif choice == "6":
            filter_by_category(input("Enter category: "))

        elif choice == "7":
            generate_report()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
