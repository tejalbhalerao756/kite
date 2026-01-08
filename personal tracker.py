import datetime

FILE_NAME = "expenses.txt"   

def add_expense():
    amount = float(input("Enter amount: ₹"))
    category = input("Enter category (Food, Travel, Bills, etc.): ")
    description = input("Enter description: ")

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_NAME, "a") as file:
        file.write(f"{date},{amount},{category},{description}\n")

    print("✅ Expense added successfully!")

def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            print("\nDate | Amount | Category | Description")
            print("-" * 60)
            for line in file:
                date, amount, category, desc = line.strip().split(",")
                print(f"{date} | ₹{amount} | {category} | {desc}")
    except FileNotFoundError:
        print("No expenses found.")

def total_expense():
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                _, amount, _, _ = line.strip().split(",")
                total += float(amount)
        print(f"\n💰 Total Expense: ₹{total}")
    except FileNotFoundError:
        print("No expenses found.")

def category_expense():
    cat = input("Enter category: ")
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                _, amount, category, _ = line.strip().split(",")
                if category.lower() == cat.lower():
                    total += float(amount)
        print(f"\n📊 Total expense for {cat}: ₹{total}")
    except FileNotFoundError:
        print("No expenses found.")

def menu():
    while True:
        print("\n====== PERSONAL EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Expense by Category")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            category_expense()
        elif choice == "5":
            print("👋 Thank you!")
            break
        else:
            print("Invalid choice!")

menu()

