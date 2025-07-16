import tkinter as tk
from tkinter import messagebox
from user_panel import open_user_panel
from db_config import connect_db

# signup logic
def open_user_signup():
    signup_win = tk.Toplevel()
    signup_win.title("User Signup")
    signup_win.geometry("300x220")
    signup_win.config(bg="#f5f5f5")

    tk.Label(signup_win, text="User Signup", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

    tk.Label(signup_win, text="Choose Username:", bg="#f5f5f5").pack()
    username_entry = tk.Entry(signup_win, font=("Arial", 12))
    username_entry.pack()

    tk.Label(signup_win, text="Choose Password:", bg="#f5f5f5").pack()
    password_entry = tk.Entry(signup_win, font=("Arial", 12), show="*")
    password_entry.pack()

    def signup_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Missing Info", "All fields are required.")
            return

        con = connect_db()
        cur = con.cursor()

        # Checking for user existence
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            messagebox.showerror("Username Exists", "Choose a different username.")
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            con.commit()
            messagebox.showinfo("Success", "Signup successful! You can now login.")
            signup_win.destroy()

        cur.close()
        con.close()

    tk.Button(signup_win, text="Sign Up", command=signup_user).pack(pady=10)

# login logic
def open_user_login():
    login_win = tk.Toplevel()
    login_win.title("User Login")
    login_win.geometry("300x200")
    login_win.config(bg="#f5f5f5")

    tk.Label(login_win, text="User Login", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

    tk.Label(login_win, text="Username:", bg="#f5f5f5").pack()
    username_entry = tk.Entry(login_win, font=("Arial", 12))
    username_entry.pack()

    tk.Label(login_win, text="Password:", bg="#f5f5f5").pack()
    password_entry = tk.Entry(login_win, font=("Arial", 12), show="*")
    password_entry.pack()

    def login_check():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showwarning("Missing Info", "Enter both username and password.")
            return

        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        con.close()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            login_win.destroy()
            open_user_panel(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login_win, text="Login", command=login_check).pack(pady=10)
