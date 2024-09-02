import bcrypt
from datetime import datetime, timedelta
import json
import random
import sqlite3

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

connection = sqlite3.connect('database.db')

with open('create_users_table.sql') as f:
    connection.executescript(f.read())

with open('create_posts_table.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('posts.json', 'r') as f:
    posts_data = json.load(f)

with open('users.json', 'r') as f:
    users_data = json.load(f)

user_id_map = {}
for user in users_data['users']:
    hashed_password = bcrypt.hashpw(
        user['password'].encode('utf-8'), bcrypt.gensalt())
    cur.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (user['username'], user['email'],
                 hashed_password, user['role'])
                )
    user_id_map[user['id']] = cur.lastrowid

start_date = datetime(datetime.now().year, 1, 1)
end_date = datetime.now()

for post in posts_data['posts']:
    user_id = user_id_map.get(post['userId'])
    if user_id:
        created_date = random_date(start_date, end_date)
        cur.execute("INSERT INTO posts (title, content, userId, created) VALUES (?, ?, ?, ?)",
                    (post['title'], post['body'], user_id, created_date)
                    )

connection.commit()
connection.close()
