import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create the main application window
root = tk.Tk()
root.title("Business Chatbot Setup")
root.geometry("600x400")

# Create the connection to SQLite (or MySQL as needed)
conn = sqlite3.connect('business_chatbot.db')
cursor = conn.cursor()

# Create a table for FAQs (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
''')
conn.commit()

# Function to add an FAQ
def add_faq():
    question = entry_question.get()
    answer = entry_answer.get()
    if question and answer:
        cursor.execute('INSERT INTO faqs (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
        messagebox.showinfo("Success", "FAQ added successfully!")
        entry_question.delete(0, tk.END)
        entry_answer.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both a question and an answer.")

# GUI Components
label_question = tk.Label(root, text="Enter Question:")
label_question.pack(pady=10)
entry_question = tk.Entry(root, width=50)
entry_question.pack(pady=10)

label_answer = tk.Label(root, text="Enter Answer:")
label_answer.pack(pady=10)
entry_answer = tk.Entry(root, width=50)
entry_answer.pack(pady=10)

button_add = tk.Button(root, text="Add FAQ", command=add_faq)
button_add.pack(pady=20)

# Start the main loop
root.mainloop()

# Close the connection on exit
conn.close()
