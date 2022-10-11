import sqlite3


class DB():
    schema = '''
        CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER PRIMARY KEY,
            user_name TEXT NOT NULL,
            password TEXT NOT NULL
);'''

conn = sqlite3.connect('users.db')
cur = conn.cursor()

with open('schema.sql', 'r') as f:
    cur.executescript(f.read())

cur.execute('''
            INSERT INTO user (user_name, password) VALUES
                                                    ("jaybird", "testing"),
                                                    ("user", "password"),
                                                    ("user3", "test")
            ''')

conn.commit()

#cur.execute('INSERT INTO users (user_name, password) VALUES ("jaybird","testing")')
#
#cur.execute('SELECT * FROM users')