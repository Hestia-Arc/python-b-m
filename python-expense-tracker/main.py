import os
import json
import uuid

# ======================
#  LOAD USER
# ======================
def loadUser():
    if os.path.exists("user.json"):
        with open("user.json", "r") as file:
            userData = json.load(file)

        print(f"Welcome back, {userData['name']}\n")
    
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

# ======================
# ADD EXPENSE
# ======================
def addExpense():

    # ===========================================
    # prompt user for an expense amt/category/desc
    # validate
    # save expense to a file
    # print

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

        except ValueError():
            print("Description cannot be empty")

    expense = {
        "id": str(uuid.uuid4),
        "amount": expenseAmt,
        "category": expenseCat,
        "description": expenseDesc
    }

    # save to a file
    data.append(expense)

    with open("expenseData.json", "w") as file:
        json.dump(data, file, indent=4)

    return f"\n{expense['description']} added.\n"


# ======================
# DELETE EXPENSE
# ======================
def deleteExpense(expenseDesc):

    with open("expenseData.json", "r") as file:
        data = json.load(file)

        expenseList = len(data)
        data = [expense for expense in data if expense.get("description") != expenseDesc]

        if len(data) == expenseList:
            return "Expense not found."
        
        with open("expenseData.json", "w") as file:
            json.dump(data, file, indent=4)

    return "Expense deleted."

# ======================
# VIEW ALL EXPENSES
# ======================
def viewAllExpenses():
    
    with open("expenseData.json", "r") as file:
        data = json.load(file)

        return data

# ======================
# CAL BY CATEGORY
# ======================
def calByCategory():
    return "Calculated."


# PROGRAM BEGINS
def main():
    # check/load user when program starts
    loadUser()

    # load expense when program starts
    if os.path.exists("expenseData.json"):
        try:
            with open("expenseData.json", "r") as file:
                data = json.load(file)
                
                print("Loading expenses...\n")
                print("----------------------------------------")
                print("| NO | DESC  |   AMOUNT   |   CATEGORY |")
                print("----------------------------------------")


            for expense in data:
                # print(f"{expense['desc']}")
                print(f"{expense['description']}---{expense['amount']}---{expense['category']} ")
                print(f"----------------------")

            print(f"TOTAL SPENT: {sum(expense['amount'] for expense in data)}")

        except json.JSONDecodeError:
            print("Invalid json")

    else:
        data = []

        with open("expenseData.json", "w") as file:
            json.dump(data, file, indent=4)

            print("No expense found.\n")

    # prompt user for action
    while True:
        print("\nWhat would you like to do?")

        print("1. Add an expense")
        print("2. Delete an expense")
        print("3. View all expenses")
        print("4. Calculate by category")
        print("5. Exit")

        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            print(addExpense())

        elif choice == 2:
            expenseToDelete = input("Specify expense description: ")
            print(deleteExpense(expenseToDelete))

        elif choice == 3:
            data = viewAllExpenses()

            print("\nLoading expenses...\n")
            print("----------------------------------------")
            print("| NO | DESC  |   AMOUNT   |   CATEGORY |")
            print("----------------------------------------")

            for expense in data:
                print(f"{expense['description']}---{expense['amount']}---{expense['category']} ")
                print(f"----------------------")

            print(f"TOTAL SPENT: {sum(expense['amount'] for expense in data)}")
            

        elif choice == 4:
            print(calByCategory())

        elif choice == 5:
            print("\nShutting down...")
            break



if __name__ == '__main__':
    main()