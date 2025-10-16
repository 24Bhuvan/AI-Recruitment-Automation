import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # replace with your MySQL username
    password="pass123",  # replace with your MySQL password
    database="airesumescreening"
)

cursor = conn.cursor()

# Test connection
try:
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    print(f"Connected to database: {db_name[0]}")
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Close connection
cursor.close()
conn.close()
