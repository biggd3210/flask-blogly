"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
    
    image_url = db.Column(db.String(100),
                          nullable=True,
                          default="https://www.pngwing.com/en/free-png-zlrqq")
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} f_name={u.first_name} l_name={u.last_name}"
    
    # ******** class methods go here: *********

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).all()
    


    # ******** instance methods go here *********

    def make_full_name(self):
        first = self.first_name
        last = self.last_name
        return f"{first} {last}"