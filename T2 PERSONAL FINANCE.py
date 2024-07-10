import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Create GUI components
        self.income_label = tk.Label(root, text="Income:")
        self.income_label.grid(row=0, column=0)
        self.income_entry = tk.Entry(root, width=20)
        self.income_entry.grid(row=0, column=1)

        self.expense_label = tk.Label(root, text="Expense:")
        self.expense_label.grid(row=1, column=0)
        self.expense_entry = tk.Entry(root, width=20)
        self.expense_entry.grid(row=1, column=1)

        self.savings_label = tk.Label(root, text="Savings:")
        self.savings_label.grid(row=2, column=0)
        self.savings_entry = tk.Entry(root, width=20)
        self.savings_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.view_button = tk.Button(root, text="View Transactions", command=self.view_transactions)
        self.view_button.grid(row=4, column=0, columnspan=2)

        self.graph_button = tk.Button(root, text="View Graph", command=self.view_graph)
        self.graph_button.grid(row=5, column=0, columnspan=2)

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                date TEXT,
                income REAL,
                expense REAL,
                savings REAL
            )
        """)
        self.conn.commit()

    def add_transaction(self):
        income = self.income_entry.get()
        expense = self.expense_entry.get()
        savings = self.savings_entry.get()
        if income and expense and savings:
            self.cursor.execute("""
                INSERT INTO transactions (date, income, expense, savings)
                VALUES (DATE('now'), ?, ?, ?)
            """, (income, expense, savings))
            self.conn.commit()
            self.income_entry.delete(0, tk.END)
            self.expense_entry.delete(0, tk.END)
            self.savings_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def view_transactions(self):
        self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()
        for transaction in transactions:
            print(transaction)

    def view_graph(self):
        self.cursor.execute("SELECT date, income, expense, savings FROM transactions")
        transactions = self.cursor.fetchall()
        dates = [transaction[0] for transaction in transactions]
        incomes = [transaction[1] for transaction in transactions]
        expenses = [transaction[2] for transaction in transactions]
        savings = [transaction[3] for transaction in transactions]

        plt.plot(dates, incomes, label="Income")
        plt.plot(dates, expenses, label="Expense")
        plt.plot(dates, savings, label="Savings")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Personal Finance Graph")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()