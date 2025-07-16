import tkinter as tk
from user_panel import open_user_panel
from admin_panel import open_admin_panel
from auth import open_user_login, open_user_signup

# Main Window
def main_window():
    root = tk.Tk()
    root.title("Canteen Meal Ordering")
    root.geometry("300x200")
    root.config(bg="#f5f5f5")

    # Title
    tk.Label(root, text="Choose your role", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=20)

    # Buttons
# User login and signup
    tk.Button(root, text="User Login", font=("Arial", 12), width=20, command=open_user_login).pack(pady=5)
    tk.Button(root, text="User Signup", font=("Arial", 12), width=20, command=open_user_signup).pack(pady=5)
    tk.Button(root, text="Admin", font=("Arial", 12), width=20, command=open_admin_panel).pack()

    root.mainloop()

if __name__ == "__main__":
    main_window()
