from datetime import datetime
from app.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def formatted_created(self):
        return self.created.strftime("%d-%m-%Y %H:%M")

    def __repr__(self):
        return f'<Post "{self.title}">'