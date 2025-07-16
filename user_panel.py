import tkinter as tk
from tkinter import messagebox
from db_config import connect_db

# Menu items
menu_items = [
    {"name": "Tea", "price": 10},
    {"name": "Coffee", "price": 15},
    {"name": "Fried Rice", "price": 60},
    {"name": "Veg Meals", "price": 50},
    {"name": "Chicken Biryani", "price": 90},
    {"name": "Idli", "price": 5}
]

# function to open user panel
def open_user_panel(username):
    user_win = tk.Toplevel()
    user_win.title("User - Place Order")
    user_win.geometry("420x650")
    user_win.config(bg="#f5f5f5")

    tk.Label(user_win, text="Place Your Order", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    items_frame = tk.Frame(user_win, bg="#f5f5f5")
    items_frame.pack()

    quantities = []
    item_totals = []
    total_var = tk.StringVar()
    total_var.set("Total: ₹ 0")

    def update_total():
        total = 0
        i = 0
        while i < len(menu_items):
            qty = quantities[i].get()
            price = menu_items[i]["price"]
            cost = qty * price
            item_totals[i].set("₹ " + str(cost))
            total += cost
            i += 1
        total_var.set("Total: ₹ " + str(total))

    i = 0
    while i < len(menu_items):
        item = menu_items[i]

        frame = tk.Frame(items_frame, bd=1, relief="solid", bg="#ffffff", padx=10, pady=5)
        frame.pack(pady=5, padx=10, fill="x")

        tk.Label(frame, text=item["name"], font=("Arial", 12, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text="₹" + str(item["price"]), font=("Arial", 10), bg="#ffffff").grid(row=0, column=1)

        qty_var = tk.IntVar()
        qty_var.set(0)
        quantities.append(qty_var)

        total_label = tk.StringVar()
        total_label.set("₹ 0")
        item_totals.append(total_label)

        def make_increase_function(index):
            def increase():
                quantities[index].set(quantities[index].get() + 1)
                update_total()
            return increase

        def make_decrease_function(index):
            def decrease():
                if quantities[index].get() > 0:
                    quantities[index].set(quantities[index].get() - 1)
                    update_total()
            return decrease

        tk.Button(frame, text="-", command=make_decrease_function(i), width=2).grid(row=1, column=0)
        tk.Label(frame, textvariable=qty_var, width=3, bg="#ffffff").grid(row=1, column=1)
        tk.Button(frame, text="+", command=make_increase_function(i), width=2).grid(row=1, column=2)
        tk.Label(frame, textvariable=total_label, font=("Arial", 10), bg="#ffffff").grid(row=1, column=3, padx=10)

        i += 1

    tk.Label(user_win, textvariable=total_var, font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=15)

    def submit_order():
        name = username
        con = connect_db()
        cur = con.cursor()

        total_cost = 0
        has_order = False
        order_details = []
        inserted_ids = []

        i = 0
        while i < len(menu_items):
            qty = quantities[i].get()
            if qty > 0:
                item_name = menu_items[i]["name"]
                item_price = menu_items[i]["price"]
                item_total = qty * item_price
                total_cost += item_total
                has_order = True
                order_details.append((name, item_name, qty, item_total))
            i += 1

        if not has_order:
            messagebox.showwarning("No Order", "Please select at least one item.")
            return

        try:
            j = 0
            while j < len(order_details):
                cur.execute(
                    "INSERT INTO orders (customer_name, item_name, quantity, total_price) VALUES (%s, %s, %s, %s)",
                    order_details[j]
                )
                inserted_ids.append(cur.lastrowid)
                j += 1

            kot_number = "KOT-" + str(1000 + inserted_ids[0])

            for order_id in inserted_ids:
                cur.execute("UPDATE orders SET kot_number = %s WHERE id = %s", (kot_number, order_id))

            con.commit()

            messagebox.showinfo("Order Placed ", "Your KOT Number is: " + kot_number + "\n\nShow this at the counter.")

        except Exception as e:
            con.rollback()
            messagebox.showerror("Error", "Order failed: " + str(e))
        finally:
            cur.close()
            con.close()

    tk.Button(user_win, text="Place Order", font=("Arial", 12), command=submit_order).pack(pady=10)

    def view_my_orders():
        con = connect_db()
        cur = con.cursor()

        try:
            cur.execute(
                "SELECT item_name, quantity, total_price, kot_number, order_status FROM orders WHERE customer_name = %s ORDER BY order_time DESC",
                (username,)
            )
            orders = cur.fetchall()

            if len(orders) == 0:
                messagebox.showinfo("No Orders", "You haven't placed any orders yet.")
                return

            order_win = tk.Toplevel()
            order_win.title("My Orders")
            order_win.geometry("500x350")
            order_win.config(bg="#f5f5f5")

            tk.Label(order_win, text="Orders for " + username, font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

            frame = tk.Frame(order_win, bg="#ffffff", bd=1, relief="solid")
            frame.pack(padx=10, pady=10, fill="both", expand=True)

            headers = ["Item", "Qty", "Total", "KOT", "Status"]
            col = 0
            while col < len(headers):
                tk.Label(frame, text=headers[col], font=("Arial", 10, "bold"), bg="#ddd", width=10, bd=1, relief="solid").grid(row=0, column=col)
                col += 1

            row_index = 1
            while row_index <= len(orders):
                order = orders[row_index - 1]
                col_index = 0
                while col_index < len(order):
                    tk.Label(frame, text=str(order[col_index]), bg="#fff", width=10, bd=1, relief="solid").grid(row=row_index, column=col_index)
                    col_index += 1
                row_index += 1

        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch orders: " + str(e))
        finally:
            cur.close()
            con.close()

    tk.Button(user_win, text="My Orders", font=("Arial", 12), command=view_my_orders).pack(pady=5)
