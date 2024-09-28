import math

class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.balance = 0
        
    def __str__(self):
        self.title_line = f'{self.category.center(30, "*")}\n'
        self.list = ""
        for transaction in self.ledger:
            self.list += transaction['description'].ljust(23)[:23] + ("%.2f"%(transaction['amount'])).rjust(7) + '\n'
        self.total_line = 'Total: ' + "%.2f"%self.balance
        return f'{self.title_line}{self.list}{self.total_line}'
    
    def check_funds(self,amount):
        if amount > self.balance:
            return False
        else:
            return True
        
    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount
        return self.ledger
    
    def withdraw(self, amount, description=''):
        if amount <= self.balance:
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False
        
    def get_balance(self):
        return self.balance
    
    def transfer(self,amount, budget):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget.category}")
            budget.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False


def round_perc(num):
    if num % 10 >= 5:
        num = (num // 10)  + 1
    else:
        num = (num // 10)
    return num

def create_spend_chart(categories):
    spend_list = []

    for category in categories:
        neg_amounts = 0
        for item in category.ledger:
            if item['amount'] < 0:
                neg_amounts += abs(item['amount'])
        spend_list.append(neg_amounts)

    total_spend = sum(spend_list)
    
    # Prevent division by zero
    if total_spend == 0:
        percent_list = [0] * len(spend_list)  # If no spending, set all percentages to 0
    else:
        percent_list = [((item/total_spend) * 100) for item in spend_list]

    row_line = "Percentage spent by category"
    
    for row in range(100, -10, -10):
        row_line += '\n' + str(row).rjust(3) + '|'
        
        for column_value in percent_list:
            if column_value >= row:
                row_line += ' o '
            else:
                row_line += '   '
        row_line += ' '

    row_line += "\n    ----------"  # Bottom border of the chart

    categories_len_list = [len(category.category) for category in categories]
    max_len = max(categories_len_list)

    for row in range(max_len):
        row_line += '\n    '

        for column_item in range(len(categories)):
            if row < categories_len_list[column_item]:
                row_line += ' ' + categories[column_item].category[row] + ' '
            else:
                row_line += '   '  # Add spaces to align

        row_line += ' '
    
    return row_line



def user_interaction():
    categories = []

    # Ask for the number of categories
    num_categories = int(input("Enter the number of budget categories: "))

    # Initialize categories
    for i in range(num_categories):
        category_name = input(f"Enter the name of category {i + 1}: ")
        categories.append(Category(category_name))

    # Allow user to make transactions
    while True:
        print("\nAvailable actions: ")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Show balances")
        print("5. Create Spending Chart")
        print("6. Exit")

        action = input("Choose an action (1-6): ")

        if action == "1":
            category_index = int(input("Select a category by number: ")) - 1
            amount = float(input("Enter deposit amount: "))
            description = input("Enter description: ")
            categories[category_index].deposit(amount, description)

        elif action == "2":
            category_index = int(input("Select a category by number: ")) - 1
            amount = float(input("Enter withdrawal amount: "))
            description = input("Enter description: ")
            success = categories[category_index].withdraw(amount, description)
            if not success:
                print("Insufficient funds!")

        elif action == "3":
            from_category = int(input("Select category to transfer from: ")) - 1
            to_category = int(input("Select category to transfer to: ")) - 1
            amount = float(input("Enter transfer amount: "))
            success = categories[from_category].transfer(amount, categories[to_category])
            if not success:
                print("Insufficient funds!")

        elif action == "4":
            for i, category in enumerate(categories):
                print(f"\n{category}")

        elif action == "5":
            print(create_spend_chart(categories))

        elif action == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please select again.")

# Run the user interaction
user_interaction()
