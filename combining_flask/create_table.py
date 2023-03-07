import sqlite3

conn = sqlite3.connect('students.db')
print("opened database successfully")

conn.execute('CREATE TABLE students (user_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, addr TEXT, city TEXT)')
print ("table created successfully")
conn.close()