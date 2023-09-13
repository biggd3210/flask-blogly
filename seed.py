from models import User, Post, db
from app import app

# create all tables

db.drop_all()
db.create_all()

# empty table if not already:

User.query.delete()

# add users

dsb = User(first_name="Derek", last_name="Biggers")
jh = User(first_name="Jacob", last_name="Henry")
dh = User(first_name="Devon", last_name="Havenshire")

# add posts

post1 = Post(title="This is my first post!", content="Just wanting to see if this works.", user_id=1)
post2 = Post(title="I'm joining the convo!", content="I just like to be involved", user_id=3)

# add new objects to session so they persist

db.session.add(dsb)
db.session.add(jh)
db.session.add(dh)

# commit so the information is saved to the database.

db.session.commit()

# add post data after users are added to avoid FK constraint

db.session.add(post1)
db.session.add(post2)

# commit posts table data changes

db.session.commit()