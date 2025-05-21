# We will create the following classes:

# Bank: Manages all customers and accounts, assigns unique IDs, and provides methods for high-level operations.
# Customer: Represents a bank customer, storing their details and a list of accounts.
# Account: A base class for all account types, handling basic operations like deposits and withdrawals.
# SavingsAccount: A subclass of Account that adds interest monthly.
# CheckingAccount: A subclass of Account that deducts a monthly fee.
class Bank:
    def __init__(self, name):
        self.name = name
        self.customer = {}
        self.account = {}
        self.next_account_id = 0
        self.next_customer_id = 0
    
    def open_account(self, customer, account_type):
        account_number = self.next_account_id
        self.next_account_id += 1
        if account_type == "savings":
            account = SavingsAccount(account_number, customer)
        elif account_type == "checking":
            account = CheckingAccount(account_number, customer)
        else:
            raise ValueError("Invalid account type")
        self.accounts[account_number] = account
        customer.add_account(account)
        return account
        
    def add_customer(self, name):
        customer = Customer(name, self.next_customer_id)
        self.customer[self.next_customer_id] = customer
        self.next_customer_id += 1
        return customer
    
    def close_account(self, account_number):
        if account_number in self.accounts:
            account = self.accounts[account_number]
            customer = account.customer
            customer.remove_account(account_number)
            del self.accounts[account_number]
        else:
            raise ValueError("Account not found")
            
    def apply_monthly_operations(self):
        for account in self.accounts.values():
            account.process_monthly
        
    def transfer(self, from_account_number, to_account_number, amount):
        if from_account_number not in self.accounts or to_account_number not in self.accounts:
            raise ValueError("Account not found")
        from_account = self.accounts[from_account_number]
        to_account = self.accounts[to_account_number]
        if from_account.get_balance() >= amount:
            from_account.withdraw(amount)
            to_account.deposit(amount)
        else:
            raise ValueError("Insufficient funds")
        
class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id
        self.accounts = []
    
    
    def add_account(self, account):
        self.accounts.append(account)
    
    def remove_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                 self.accounts.remove(account)
                 return
            raise ValueError("Account not found")
    
    def get_accounts(self):
        return self.accounts
    
    def get_total_balance(self):
        return sum(account.get_balance() for account in self.accounts)
class Account:
    def __init__(self, account_number, customer):
        self.account_number = account_number
        self.customer = customer
        self.balance = 0.0
        self.transactions = []
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(("deposit", amount))
        else:
            raise ValueError("Deposit amount must be positive")
        
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append(("withdrawal", amount))
        else:
            raise ValueError("Invalid withdrawal amount")
        
    def get_balance(self):
        return self.balance
    
    def process_monthly(self):
        pass
    
class SavingsAccount(Account):
    
    def __init__(self, account_number, customer, interest_rate = 0.01):
        super().__init__(account_number, customer)
        self.interest_rate = interest_rate
    
    def process_monthly(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transactions.append(("interest", interest))
        
        
        
class CheckingAccount(Account):
    def __init__(self, account_number, customer, monthly_fee=5.0):
        super().__init__(account_number, customer)
        self.monthly_fee = monthly_fee
        
    def process_monthly(self):
        if self.balance >= self.monthly_fee:
            self.balance -= self.monthly_fee
            self.transactions.append(("fee", self.monthly_fee))
        else:
            raise ValueError("Insufficient funds for fee")