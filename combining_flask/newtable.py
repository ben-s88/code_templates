import sqlite3

conn = sqlite3.connect('login.db')
conn.execute('create table login(user_id INTEGER PRIMARY KEY AUTOINCREMENT,email text not null,password text not null);')
conn.execute('insert into login (user_id,email,password) VALUES (120,"xyz@mail.com","123xyz")')
conn.execute('insert into login (email,password) VALUES ("abc@mail.com","123abc")')
conn.commit()