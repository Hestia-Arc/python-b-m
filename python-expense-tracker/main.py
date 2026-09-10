import os
import json

# check user when program starts
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

# load expense when program starts
if os.path.exists("expenseData.json"):
    try:
        with open("expenseData.json", "r") as file:
            data = json.load(file)

            print("Loading expenses...\n")
            print(" ----------------------------------")
            print("| DESC  |   AMOUNT   |   CATEGORY |")
            print(" ----------------------------------")


        for expense in data:
            # print(f"{expense['desc']}")
            print(f"{expense['description']}---{expense['amount']}---{expense['category']} ")
            print(f"----------------------")

    except json.JSONDecodeError:
        print("Invalid json")

else:
    data = []

    with open("expenseData.json", "w") as file:
        json.dump(data, file, indent=4)

        print("No expense found.\n")

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
    "amount": expenseAmt,
    "category": expenseCat,
    "description": expenseDesc
}

# save to a file
data.append(expense)

with open("expenseData.json", "w") as file:
    json.dump(data, file, indent=4)

with open("expenseData.json", "r") as file:
    data = json.load(file)

    print("\nLoading expenses...\n")
    print(" ----------------------------------")
    print("| DESC  |   AMOUNT   |   CATEGORY |")
    print(" ----------------------------------")

    for expense in data:
        print(f"{expense['description']}---{expense['amount']}---{expense['category']} ")
        print(f"----------------------")