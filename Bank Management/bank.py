import tkinter as tk
from tkinter import messagebox

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder}\nBalance: {self.balance}"

class BankingSystem:
    def __init__(self, root):
        self.accounts = {}

        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x700")
        self.root.config(bg="#2196F3")  # Light Blue Background for window

        # Welcome Label
        self.welcome_label = tk.Label(root, text="Welcome to the Banking Management System", font=("Arial", 18, "bold"), bg="#2196F3", fg="white")
        self.welcome_label.pack(pady=20)

        # Create account section
        self.create_account_frame = tk.Frame(root, bg="#4CAF50")  # Green background for the create account frame
        self.create_account_frame.pack(pady=20)

        self.acc_num_label = tk.Label(self.create_account_frame, text="Account Number:", font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.acc_num_label.grid(row=0, column=0, padx=10, pady=10)
        self.acc_num_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 14))
        self.acc_num_entry.grid(row=0, column=1, padx=10, pady=10)

        self.acc_holder_label = tk.Label(self.create_account_frame, text="Account Holder:", font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.acc_holder_label.grid(row=1, column=0, padx=10, pady=10)
        self.acc_holder_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 14))
        self.acc_holder_entry.grid(row=1, column=1, padx=10, pady=10)

        self.initial_balance_label = tk.Label(self.create_account_frame, text="Initial Balance:", font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.initial_balance_label.grid(row=2, column=0, padx=10, pady=10)
        self.initial_balance_entry = tk.Entry(self.create_account_frame, font=("Helvetica", 14))
        self.initial_balance_entry.grid(row=2, column=1, padx=10, pady=10)

        self.create_acc_button = tk.Button(self.create_account_frame, text="Create Account", command=self.create_account, font=("Helvetica", 14, "bold"), bg="#8BC34A", fg="white", relief="solid", width=20)
        self.create_acc_button.grid(row=3, columnspan=2, pady=20)

        # Transaction section
        self.transaction_frame = tk.Frame(root, bg="#FF9800")  # Orange background for transaction frame
        self.transaction_frame.pack(pady=20)

        self.trans_acc_num_label = tk.Label(self.transaction_frame, text="Account Number:", font=("Helvetica", 14), bg="#FF9800", fg="white")
        self.trans_acc_num_label.grid(row=0, column=0, padx=10, pady=10)
        self.trans_acc_num_entry = tk.Entry(self.transaction_frame, font=("Helvetica", 14))
        self.trans_acc_num_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_label = tk.Label(self.transaction_frame, text="Amount:", font=("Helvetica", 14), bg="#FF9800", fg="white")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.transaction_frame, font=("Helvetica", 14))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.deposit_button = tk.Button(self.transaction_frame, text="Deposit", command=self.deposit, font=("Helvetica", 14, "bold"), bg="#2196F3", fg="white", relief="solid", width=20)
        self.deposit_button.grid(row=2, column=0, pady=20)

        self.withdraw_button = tk.Button(self.transaction_frame, text="Withdraw", command=self.withdraw, font=("Helvetica", 14, "bold"), bg="#F44336", fg="white", relief="solid", width=20)
        self.withdraw_button.grid(row=2, column=1, pady=20)

        # Account Info section
        self.info_frame = tk.Frame(root, bg="#9C27B0")  # Purple background for account info frame
        self.info_frame.pack(pady=20)

        self.info_acc_num_label = tk.Label(self.info_frame, text="Account Number:", font=("Helvetica", 14), bg="#9C27B0", fg="white")
        self.info_acc_num_label.grid(row=0, column=0, padx=10, pady=10)
        self.info_acc_num_entry = tk.Entry(self.info_frame, font=("Helvetica", 14))
        self.info_acc_num_entry.grid(row=0, column=1, padx=10, pady=10)

        self.info_button = tk.Button(self.info_frame, text="Display Info", command=self.display_info, font=("Helvetica", 14, "bold"), bg="#D32F2F", fg="white", relief="solid", width=20)
        self.info_button.grid(row=1, columnspan=2, pady=20)

    def create_account(self):
        acc_num = self.acc_num_entry.get()
        acc_holder = self.acc_holder_entry.get()
        initial_balance = self.initial_balance_entry.get()

        try:
            initial_balance = float(initial_balance)
            if acc_num and acc_holder:
                self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
                messagebox.showinfo("Success", "Account created successfully!")
            else:
                messagebox.showwarning("Error", "Account number and holder name cannot be empty!")
        except ValueError:
            messagebox.showwarning("Error", "Initial balance must be a valid number!")

    def deposit(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = self.amount_entry.get()

        try:
            amount = float(amount)
            if acc_num in self.accounts:
                self.accounts[acc_num].deposit(amount)
                messagebox.showinfo("Success", f"Deposited {amount}. New balance is {self.accounts[acc_num].get_balance()}.")
            else:
                messagebox.showwarning("Error", "Account not found!")
        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get()
        amount = self.amount_entry.get()

        try:
            amount = float(amount)
            if acc_num in self.accounts:
                self.accounts[acc_num].withdraw(amount)
                messagebox.showinfo("Success", f"Withdrew {amount}. New balance is {self.accounts[acc_num].get_balance()}.")
            else:
                messagebox.showwarning("Error", "Account not found!")
        except InsufficientFundsError as e:
            messagebox.showwarning("Error", str(e))
        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def display_info(self):
        acc_num = self.info_acc_num_entry.get()

        if acc_num in self.accounts:
            account_info = self.accounts[acc_num].display_account_info()
            messagebox.showinfo("Account Info", account_info)
        else:
            messagebox.showwarning("Error", "Account not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
