from typing import Optional


def add(num1: int, num2: int) -> int:
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    return num1 / num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance: Optional[int | float] = 0):
        self.balance = starting_balance
    
    def deposit(self, amount: Optional[int | float]):
        self.balance += amount
    
    def withdraw(self, amount: Optional[int | float]):
        if self.balance < amount:
            raise InsufficientFunds("Insufficient funds")
            # raise ZeroDivisionError("Insufficient funds")
        self.balance -= amount
    
    def interest(self) -> float:
        self.balance *= 1.1
        self.balance = round(self.balance, 1)