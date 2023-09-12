from models import User, db
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

# add new objects to session so they persist

db.session.add(dsb)
db.session.add(jh)
db.session.add(dh)

# commit so the information is saved to the database.

db.session.commit()