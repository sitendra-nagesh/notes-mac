import pytest
from app.calculations import add, multiply, subtract, divide, BankAccount, InsufficientFunds

@pytest.fixture
def defaut_bank_account():
    # return the instance of BankAccount
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 4, 7),
    (6, 7, 13),
    (0, 0, 0),
    (-1, 1, 0),
    (-71, -29, -100)]
)
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_subtract(): 
    print("Testing subtract function")
    assert subtract(3, 9) == -6

def test_multiply():
    print("Testing multiply function")
    assert multiply(3, 4) == 12

def test_divide():
    print("Testing divide function")
    assert divide( 2, 5) == 0.4

# testing from class
def test_initial_bank_balance(bank_account):
    assert bank_account.balance == 50

def test_default_bank_balance(defaut_bank_account):
    assert defaut_bank_account.balance == 0

def test_bank_deposit(bank_account):
    bank_account.deposit(70)
    assert bank_account.balance == 120

def test_bank_withdraw(bank_account):   
    bank_account.withdraw(40)
    assert bank_account.balance == 10

def test_bank_interest(bank_account):
    bank_account.interest()
    assert bank_account.balance == 55

@pytest.mark.parametrize("deposited, withdrew, expected",  [
    (200, 100, 100),
    (0, 0, 0),
    (90, 45, 45),
    (130, 113, 17)
])
def test_bank_transaction(defaut_bank_account, deposited, withdrew, expected):
    defaut_bank_account.deposit(deposited)
    defaut_bank_account.withdraw(withdrew)
    assert defaut_bank_account.balance == expected

def test_bank_insufficient_balance(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
    