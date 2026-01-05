import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv, os
import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = "expenses.csv"

# ---------- CSV Setup ----------
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])

def load_expenses():
    data = []
    with open(FILE_NAME, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def save_expense(date, amount, category, description):
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, description])

def save_all(expenses):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])
        writer.writerows(expenses)


# ---------- GUI ----------
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("750x550")
        self.root.config(bg="#e8f5ff")

        title = tk.Label(root, text="Expense Tracker", font=("Arial", 16, "bold"), bg="#e8f5ff")
        title.pack(pady=10)

        # ---------- Input Form ----------
        form = tk.Frame(root, bg="#e8f5ff")
        form.pack()

        tk.Label(form, text="Date:", bg="#e8f5ff").grid(row=0, column=0)
        self.date = DateEntry(form, date_pattern="dd-mm-yyyy")
        self.date.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Amount:", bg="#e8f5ff").grid(row=1, column=0)
        self.amount = tk.Entry(form)
        self.amount.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Category:", bg="#e8f5ff").grid(row=2, column=0)
        self.category = ttk.Combobox(form, values=[
            "Food", "Transport", "Shopping", "Bills", "Groceries",
            "Entertainment", "Medicine", "Education", "EMI", "Other"
        ])
        self.category.grid(row=2, column=1, padx=5)
        self.category.set("Food")

        tk.Label(form, text="Description:", bg="#e8f5ff").grid(row=3, column=0)
        self.description = tk.Entry(form)
        self.description.grid(row=3, column=1, padx=5)

        # ---------- Buttons ----------
        btns = tk.Frame(root, bg="#e8f5ff")
        btns.pack(pady=10)

        tk.Button(btns, text="Add Expense", width=15, command=self.add_expense).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Delete Selected", width=15, command=self.delete_expense).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Show Summary", width=15, command=self.show_summary).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="Pie Chart", width=15, command=self.show_pie_chart).grid(row=0, column=3, padx=5)
        tk.Button(btns, text="Export Excel", width=15, command=self.export_excel).grid(row=0, column=4, padx=5)

        # ---------- Table ----------
        self.tree = ttk.Treeview(root, columns=("Date","Amount","Category","Description"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.column("Amount", width=90)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_table()

    # ---------- Functions ----------
    def load_table(self):
        self.tree.delete(*self.tree.get_children())
        for (d, amt, cat, desc) in load_expenses():
            self.tree.insert("", tk.END, values=(d, f"₹ {amt}", cat, desc))

    def add_expense(self):
        date = self.date.get()
        amount = self.amount.get()
        category = self.category.get().strip()
        description = self.description.get().strip()

        if not amount or not category or not description:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        save_expense(date, amount, category, description)
        self.load_table()

        self.amount.delete(0, tk.END)
        self.description.delete(0, tk.END)
        messagebox.showinfo("Success", f"Expense Added: ₹{amount}")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select a row first!")
            return
        
        index = self.tree.index(selected)
        expenses = load_expenses()
        expenses.pop(index)
        save_all(expenses)
        self.load_table()

    def show_summary(self):
        data = load_expenses()
        if not data:
            messagebox.showinfo("Summary", "No data available!")
            return
        
        total = 0
        summary = {}
        for d, amt, cat, desc in data:
            val = float(amt)
            total += val
            summary[cat] = summary.get(cat, 0) + val
        
        msg = f"Total Spent: ₹ {total}\n\nCategory Breakdown:\n"
        for cat, t in summary.items():
            msg += f"- {cat}: ₹ {t}\n"
        messagebox.showinfo("Expense Summary", msg)

    def show_pie_chart(self):
        data = load_expenses()
        if not data:
            messagebox.showinfo("Pie Chart", "No expense data!")
            return
        
        summary = {}
        for d, amt, cat, desc in data:
            summary[cat] = summary.get(cat, 0) + float(amt)
        
        labels = list(summary.keys())
        values = list(summary.values())
        
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Expense Distribution")
        plt.show()

    def export_excel(self):
        df = pd.DataFrame(load_expenses(), columns=["Date","Amount","Category","Description"])
        file = "expenses.xlsx"
        df.to_excel(file, index=False)
        messagebox.showinfo("Export", f"Excel Saved Successfully:\n{file}")


# ---------- Run ----------
root = tk.Tk()
ExpenseTracker(root)
root.mainloop()