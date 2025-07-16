import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",     
        password="your db password",     
        database="your db name"  
    )

