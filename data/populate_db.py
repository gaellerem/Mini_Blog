import json
from datetime import datetime, timedelta
import random
import sys
from app import create_app, db
from app.models import Post, User

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def populate_users_db_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()

    with app.app_context():
        for item in data:
            user = User(
                username=item['username'],
                email=item['email'],
                created=random_date(start_date, end_date)
            )
            user.password = item['password']  # Utilise le setter pour hacher le mot de passe
            db.session.add(user)

        db.session.commit()
        print("Base de données peuplée avec succès!")

def populate_posts_db_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
    with app.app_context():
        for item in data:
            post = Post(
                title= item["title"],
                content=item["content"],
                created=random_date(start_date, end_date),
                user_id=item['user_id']
            )
            db.session.add(post)
        db.session.commit()
        print("Base de données peuplée avec succès!")

app = create_app()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == 'users':
            populate_users_db_from_json(sys.argv[2])
        elif sys.argv[1] == 'posts':
            populate_posts_db_from_json(sys.argv[2])
        else :
            print('Usage: populate_db.py <users||posts> <FILENAME.json>')
    else :
        print('Usage: populate_db.py <users||posts> <FILENAME.json>')
