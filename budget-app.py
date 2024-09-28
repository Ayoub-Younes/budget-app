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
        if amount < self.balance:
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
        
    

#------------------------------------------------
food = Category('Food')
auto = Category("Auto")
clothing = Category("Clothing")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
food.transfer(50,clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto.deposit(1000, "initial deposit")
auto.withdraw(15, 'fuel')

#------------------------------------------------
def round_perc(num):
    if num % 10 >= 5:
        num = (num // 10)  + 1
    else:
        num = (num // 10)
    return num

def add_o(num,p):
    if num >= p:return "o"
    else:return " "


#------------------------------------------------
def create_spend_chart(categories):

  spend_list = []

  for category in categories:
    neg_amounts = 0
    for item in category.ledger:
      if item['amount'] < 0:
        neg_amounts += abs(item['amount'])
    spend_list.append(neg_amounts)
        
  print(spend_list)
  # [26.04, 50]
  # 26.04 is from Food, 50 is from Clothing
  
  total_spend = sum(spend_list)
  print(total_spend)
  # 76.03999999999999

  percent_list = [((item/total_spend) * 100) for item in spend_list]

  print(percent_list)
  # [34.24513413992636, 65.75486586007365]
  
  # Use for loop within a for loop, to create a grid
  row_line = "Percentage spent by category" 
  
  for row in range(100, -10, -10):
    row_line += '\n' + str(row).rjust(3) + '|' 
    
    for column_value in percent_list:
      if column_value > row: # e.g. row is moving 100, 90, 80, etc. 
        row_line += ' o ' # e.g. if 34 > then 30, then 20, then 10, we'll add o
      else:
        row_line += '   '
    row_line += ' '
  row_line += "\n    ----------" # new line and 4 spaces because 100| then ---

  categories_len_list = [] 

  for category in categories:
    categories_len_list.append(len(category.category))
    
  max_len = max(categories_len_list)
  
  print(categories_len_list)
  # [4, 8]

  print(max_len) # this determines the rows for our bottom grid
  # 8

  for row in range(max_len): # creates rows 0, 1, 2, 3, 4, 5, 6, 7, 8
    row_line += '\n    '

    for column_item in range(len(categories)): # [Food, Clothing] = 2, loops 0 to 2, to create 2 columns
      if row < categories_len_list[column_item]: # [4, 8], first column is food, if 0 < 4, to create 4 rows
        row_line += ' ' + categories[column_item].category[row] + ' ' 
        # first column is food [loops from 0 to 2].current category is food [loops through 0 to 4, adding each letter per row]
        # categories is our list [Food, Clothing], .category[row] is our string[index of string]
      else:
        row_line += '   ' # 3 spaces: space, letter, space
    row_line += ' '
  return row_line
  

print(f'\n{create_spend_chart([food, clothing, auto])}')



