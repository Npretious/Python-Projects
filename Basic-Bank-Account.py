### Basic Bank Account Program ###

class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        """Deposited money into the account."""
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")


    def withdraw(self, amount):
        """Withdraw money from the account."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        
    def check_balance(self):
        """Get the current account balance."""
        print(f"Account balance for {self.account_holder}: ${self.balance}")

my_account = BankAccount("Nick Sinclair", initial_balance=1000)
my_account.deposit(200)
my_account.withdraw(300)
my_account.check_balance()