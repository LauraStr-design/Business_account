# a fastapi system for account managament

import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    name: str
    address: str

class Payment(BaseModel):
    id: int
    from_account_id: int  # account id from which we are sending from
    to_account_id: int    # account id to which we are sending to
    amount_in_euros: int
    payment_date: int  # date in ISO format (YYYY-MM-DD)

def write_account_to_file(account: Account):
    with open("accounts.txt", "a") as file:
        file.write(f"{account.id}, {account.type}, {account.name}, {account.address}\n")

def read_accounts_from_file():
    accounts = []
    with open("accounts.txt", "r") as file:
        for line in file:
            id, type, name, address = line.strip().split(", ")
            accounts.append(Account(id=int(id), type=type, name=name, address=address))

    return accounts

def delete_account_from_file(Account_id_to_delete: int):
    accounts = read_accounts_from_file()
    accounts = [Account for Account in accounts if Account.id != Account_id_to_delete]
    
    with open("accounts.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.id}, {account.type} {account.name}, {account.address}\n")

if not os.path.exists("accounts.txt"):
        open("accounts.txt", "w").close()

def write_payment_to_file(Payment: Payment):
    with open("payments.txt", "a") as file:
        file.write(f"{Payment.id}, {Payment.from_account_id}, {Payment.to_account_id}, {Payment.amount_in_euros}, {Payment.payment_date}\n")

def read_payments_from_file():
    payments = []
    with open("payments.txt", "r") as file:
        for line in file:
            id, from_account_id, to_account_id, amount_in_euros, payment_date = line.strip().split(", ")
            payments.append(Payment(id=int(id), from_account_id=from_account_id, to_account_id=to_account_id, amount_in_euros=amount_in_euros, payment_date=payment_date))

    return payments

def delete_payment_from_file(payment_id_to_delete: int):
    payments = read_payments_from_file()
    payments = [Payment for Payment in payments if Payment.id != payment_id_to_delete]
    
    with open("payments.txt", "w") as file:
        for Payment in payments:
            file.write(f"{Payment.id}, {Payment.from_account_id}, {Payment.to_account_id}, {Payment.amount_in_euros}, {Payment.payment_date}\n")
            
if not os.path.exists("payments.txt"):
        open("payments.txt", "w").close()

# type hint for a list of accounts
accounts:list[Account] = read_accounts_from_file()
payments:list[Payment] = read_payments_from_file()

@app.post("/accounts/")
def create_account(account: Account):
    accounts.append(account)
    write_account_to_file(account)
    return {"message": "Account created successfully"}

@app.get("/accounts/")
def get_accounts():
    return accounts

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    for account in accounts:
        if account.id == account_id:
            return account
    return {"message": "Account not found"}

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    accounts[:] = [account for account in accounts if account.id != account_id]
    return {"message": "Account deleted successfully"}

@app.post("/payments/")
def create_payment(payment: Payment):
    payments.append(payment)
    write_payment_to_file(payment)
    return {"message": "Payment created successfully"}

@app.get("/payments/")
def get_payments():
    return payments

@app.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    for payment in payments:
        if payment.id == payment_id:
            return payment
    return {"message": "Payment not found"}

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    payments[:] = [payment for payment in payments if payment.id != payment_id]
    return {"message": "Payment deleted successfully"}
