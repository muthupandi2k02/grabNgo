# grabNgo (Python + Tkinter + MySQL)
A GUI-based desktop application designed to streamline meal ordering in college canteens and organizational cafeterias. It allows users to pre-order meals, receive a unique KOT number, and track their order status. Admins can manage, update, or delete orders upon collection.

# Tech Stack
- Python 3
- Tkinter (for GUI)
- MySQL (Database)
- mysql-connector-python (for DB connection)

# Features
- User Signup & Login  
- Place orders from a dynamic menu  
- Real-time cost calculation  
- Unique KOT number for every order  
- Track order status in real time  
- Admin panel to update/delete orders
- 
# Folder Structure
grabNgo/
├── main.py
├── db_config.py
├── user_panel.py
├── admin_panel.py
├── auth.py

# How to Run the Project
1. **Clone the repository**  
```bash
git clone https://github.com/your-username/grabNgo.git
cd grabNgo
```
2. **Set up MySQL and Database**  
In your MySQL, create the following table:

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    item_name VARCHAR(100),
    quantity INT,
    total_price INT,
    kot_number VARCHAR(20) UNIQUE,
    order_status VARCHAR(20) DEFAULT 'pending',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
 # Future Enhancements
- Add PDF export of orders
- Add image thumbnails for menu items
- Add sound notification for order ready
