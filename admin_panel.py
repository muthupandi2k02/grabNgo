import tkinter as tk
from tkinter import messagebox
from db_config import connect_db

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Function to show the admin dashboard
def show_admin_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Admin Panel")
    dashboard.geometry("700x500")
    dashboard.config(bg="#f5f5f5")

    tk.Label(dashboard, text="Admin Dashboard - Orders", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    # Frame for order list
    order_frame = tk.Frame(dashboard, bg="#ffffff", bd=1, relief="solid")
    order_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Table Headers
    headers = ["ID", "Customer", "Item", "Qty", "Total", "KOT", "Status", "Action"]
    for col in range(len(headers)):
        tk.Label(order_frame, text=headers[col], font=("Arial", 10, "bold"), bg="#ddd", width=10, bd=1, relief="solid").grid(row=0, column=col)

    # Fetch orders from database
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT id, customer_name, item_name, quantity, total_price, kot_number, order_status FROM orders ORDER BY order_time DESC")
    orders = cur.fetchall()
    cur.close()
    con.close()

    status_options = ["Pending", "Ready", "Collected"]
    status_vars = []

    i = 1
    while i <= len(orders):
        order = orders[i - 1]
        order_id, customer, item, qty, total, kot, status = order

        # Create label widgets
        tk.Label(order_frame, text=order_id, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=0)
        tk.Label(order_frame, text=customer, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=1)
        tk.Label(order_frame, text=item, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=2)
        tk.Label(order_frame, text=qty, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=3)
        tk.Label(order_frame, text=total, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=4)
        tk.Label(order_frame, text=kot, bg="#fff", width=10, bd=1, relief="solid").grid(row=i, column=5)

        var = tk.StringVar()
        var.set(status)
        status_vars.append(var)

        dropdown = tk.OptionMenu(order_frame, var, *status_options)
        dropdown.config(width=10)
        dropdown.grid(row=i, column=6)

        # Update button
        def make_update_function(row_index, order_id_local):
            def update_status():
                new_status = status_vars[row_index].get()

                con2 = connect_db()
                cur2 = con2.cursor()

                try:
                    if new_status == "Collected":
                        cur2.execute("DELETE FROM orders WHERE id = %s", (order_id_local,))
                        messagebox.showinfo("Deleted", f"Order ID {order_id_local} marked as Collected and deleted.")
                    else:
                        cur2.execute("UPDATE orders SET order_status = %s WHERE id = %s", (new_status, order_id_local))
                        messagebox.showinfo("Updated", f"Order ID {order_id_local} status updated to '{new_status}'.")

                    con2.commit()
                except Exception as e:
                    con2.rollback()
                    messagebox.showerror("Error", str(e))
                finally:
                    cur2.close()
                    con2.close()

                dashboard.destroy()
                show_admin_dashboard()  # Refresh dashboard

            return update_status

        tk.Button(order_frame, text="Update", command=make_update_function(i - 1, order_id)).grid(row=i, column=7)
        i += 1

# Function to check login
def check_admin_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        login_window.destroy()
        show_admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open admin login window
def open_admin_panel():
    global login_window, username_entry, password_entry

    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    login_window.geometry("300x200")
    login_window.config(bg="#f5f5f5")

    tk.Label(login_window, text="Admin Login", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

    tk.Label(login_window, text="Username:", bg="#f5f5f5").pack()
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack()

    tk.Label(login_window, text="Password:", bg="#f5f5f5").pack(pady=(10, 0))
    password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", font=("Arial", 12), command=check_admin_login).pack(pady=15)
