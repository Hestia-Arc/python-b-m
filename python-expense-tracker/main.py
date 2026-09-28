import os
import json
import uuid
from datetime import datetime

# ======================
#  LOAD USER
# ======================
def loadUser():
    if os.path.exists("user.json"):
        with open("user.json", "r") as file:
            user = json.load(file)

        print(f"Welcome back, {user['name']}\n")

        return f"Welcome back, {user['name']}\n"

    else:
        name = input("Enter your name: ")
        role = input("Your occupation: ")

        user = {
            "name": name,
            "role": role
        }

        with open("user.json", "w") as file:
            json.dump(user, file, indent=4)

        print(f"\nWelcome, {user['name']}!\n")

    return f"\nWelcome, {user['name']}!\n"

# ======================
# PRINTING EXPENSES TEMPLATE
# ======================
def showExpenses(data):
    if not data:
        print("No expense found.\n")
        return

    print("Loading expenses...\n")
    print("------------------------------------------------")
    print("| NO | DESC            | AMOUNT   | CATEGORY   |")
    print("------------------------------------------------")

    for index, expense in enumerate(data, start=1):
        desc = expense['description'][:15]
        cat = expense['category'][:10]
        print(f"| {index:<2} | {desc:<15} | {expense['amount']:<8} | {cat:<10} |")
        print("------------------------------------------------")

    total = sum(expense['amount'] for expense in data)
    print(f"TOTAL SPENT: {total}")

# ======================
#  LOAD EXPENSES
# ======================
def loadExpenses():
    if os.path.exists("expenseData.json"):
        try:
            with open("expenseData.json", "r") as file:
                data = json.load(file)

            showExpenses(data)

        except json.JSONDecodeError:
            print("Invalid json")

    else:
        data = []
        with open("expenseData.json", "w") as file:
            json.dump(data, file, indent=4)

        print("No expense found.\n")

# ======================
# ADD EXPENSE
# ======================
def addExpense():

    # ===========================================
    # prompt user for an expense amt/category/desc
    # validate
    # save expense to a file
    # print

    if os.path.exists("expenseData.json"):
        with open("expenseData.json", "r") as file:
            data = json.load(file)
    else:
        data = []

    # expenseName = input("Add expense: ")
    while True:
        try:
            expenseAmt = int(input("\nEnter an expense amount: "))

            if expenseAmt > 0:
                break

            print("Please enter a valid number")

        except ValueError:
            print("Amount cannot be empty.\n")

    while True:
        try:
            expenseCat = input("Specify category: ").strip()

            if expenseCat != "":
                break

            print("Category cannot be empty")

        except ValueError:
            print("Category cannot be empty")

    while True:
        try:
            expenseDesc = input("Short desc: ").strip()

            if expenseDesc != "":
                break

            print("Description cannot be empty")

        except ValueError:
            print("Description cannot be empty")

    expense = {
        "id": str(uuid.uuid4()),
        "amount": expenseAmt,
        "category": expenseCat.capitalize(),
        "description": expenseDesc.capitalize(),
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # save to a file
    data.append(expense)

    with open("expenseData.json", "w") as file:
        json.dump(data, file, indent=4)

    return f"\n{expense['description']} added.\n"

# ======================
# DELETE EXPENSE
# ======================
def deleteExpense(expenseIdx):

    with open("expenseData.json", "r") as file:
        data = json.load(file)

    if expenseIdx < 0 or expenseIdx >= len(data):
        return "Expense not found."

    deletedExpense = data.pop(expenseIdx)

    with open("expenseData.json", "w") as file:
        json.dump(data, file, indent=4)

    return f"{deletedExpense['description']} deleted."


# ======================
# VIEW ALL EXPENSES
# ======================
def viewAllExpenses():

    with open("expenseData.json", "r") as file:
        data = json.load(file)

    showExpenses(data)

# ======================
# CAL BY CATEGORY
# ======================
def calByCategory(category):
    with open("expenseData.json", "r") as file:
        data = json.load(file)

    category_name = category.strip().lower()
    filtered = [
        expense for expense in data
        if expense.get("category", "").strip().lower() == category_name
    ]

    if not filtered:
        return f"No expenses found for category: {category}."

    total = sum(expense["amount"] for expense in filtered)
    return f"Total for {category}: {total}"


# PROGRAM BEGINS
def main():
    # check/load user when program starts
    loadUser()

    # load expense when program starts
    loadExpenses()

    # prompt user for action
    while True:
        print("\nWhat would you like to do?")

        print("1. Add an expense")
        print("2. Delete an expense")
        print("3. View all expenses")
        print("4. Calculate by category")
        print("5. Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            print(addExpense())

        elif choice == 2:
            try:
                expenseIndex = int(input("Enter expense index: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if expenseIndex < 1:
                print("Please enter a valid number.")
                continue

            print(deleteExpense(expenseIndex - 1))

        elif choice == 3:
            viewAllExpenses()

        elif choice == 4:
            categoryName = input("Enter category: ").strip()
            if not categoryName:
                print("Category cannot be empty.")
                continue
            print(calByCategory(categoryName))

        elif choice == 5:
            print("\nShutting down...")
            break

        else:
            print("Please enter a valid number.")



if __name__ == '__main__':
    main()