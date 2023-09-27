from models import User, Post, Tag, PostTag, db
from app import app

# create all tables

db.drop_all()
db.create_all()

# empty table if not already:

User.query.delete()
PostTag.query.delete()
Post.query.delete()
Tag.query.delete()

# add users

dsb = User(first_name="Derek", last_name="Biggers")
jh = User(first_name="Jacob", last_name="Henry")
dh = User(first_name="Devon", last_name="Havenshire")

# add posts

post1 = Post(title="This is my first post!", content="Just wanting to see if this works.", user_id=1)
post2 = Post(title="I'm joining the convo!", content="I just like to be involved", user_id=3)

# add tags

tag1 = Tag(name="new post")
tag2 = Tag(name="Funny")
tag3 = Tag(name="darkhumor")

# # add PostTags

pt1 = PostTag(post_id=1, tag_id=2)
pt2 = PostTag(post_id=2, tag_id=3)
pt3 = PostTag(post_id=1, tag_id=3)


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

# add tag data

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

# commit tag data

db.session.commit()

# add PostTag data

db.session.add(pt1)
db.session.add(pt2)
db.session.add(pt3)

# commit pts

db.session.commit()