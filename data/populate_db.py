import json
from app import db, app, User, Post
from datetime import datetime, timedelta
import random
import sys

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def populate_users_db_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    with app.app_context():
        for item in data["users"]:
            user = User(
                username=item['username'],
                email=item['email'],
                role=item['role']
            )
            user.password = item['password']  # Utilise le setter pour hacher le mot de passe
            db.session.add(user)
        
        db.session.commit()
        print("Base de données peuplée avec succès!")

def populate_posts_db_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
    with app.app_context():
        for item in data["posts"]:
            post = Post(
                title= item["title"],
                content=item["body"],
                created=random_date(start_date, end_date),
                user_id=item['userId']
            )
            db.session.add(post)
        db.session.commit()
        print("Base de données peuplée avec succès!")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'users':
            populate_users_db_from_json(sys.argv[2])
            
        elif sys.argv[1] == 'posts':
            populate_posts_db_from_json(sys.argv[2])
        else :
            print('Usage: populate_db.py <users||posts> <FILENAME.json>')
    else :
        print('Usage: populate_db.py <users||posts> <FILENAME.json>')