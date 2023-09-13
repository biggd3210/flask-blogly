"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """connects the app inherited from app.py to the proper database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)
    
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    image_url = db.Column(db.String(500),
                          nullable=True,
                          default="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/User-avatar.svg/2048px-User-avatar.svg.png")
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} f_name={u.first_name} l_name={u.last_name}"
    
    # ******** class methods go here: *********

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).all()
    


    # ******** instance methods go here *********

    @property
    def make_full_name(self):
        first = self.first_name
        last = self.last_name
        return f"{first} {last}"
    

# ******** Part Two ********* 
class Post(db.Model):
    """User model"""

    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(50),
                           nullable=False)
    
    content = db.Column(db.String,
                          nullable=False)
    
    created_at = db.Column(db.DateTime,
                          default=datetime.utcnow)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship("User", backref="posts")
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}"
    
    # ******** class methods go here: *********

    @classmethod
    def get_all_posts(cls):
        return cls.query.all()
    
    @classmethod
    def get_posts_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    


    # ******** instance methods go here *********

