"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'thisshouldbesomethingelse'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
# db.create_all()

# ******* Part One **********
@app.route('/')
def redirect_to_users():
    """redirects to users list page"""
    return redirect('/users')

@app.route('/users')
def display_all_users():
    """shows list of all users"""
    users = User.query.all()
    return render_template('users_list.html', users=users)


@app.route('/users/new')
def new_user_form():
    """displays form to create new user"""
    return render_template("create_user.html")


@app.route("/users/new", methods=['POST'])
def add_new_user():
    """collects info from form and """
    first_name = request.form['f_name']
    last_name = request.form['l_name']
    img_url = request.form['image']

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')



@app.route("/users/<int:user_id>")
def show_unique_user(user_id):
    """displays unique user page requested by user id"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    name = user.make_full_name
    return render_template("user_page.html", user=user, posts=posts, name=name)

@app.route("/users/<int:user_id>/edit")
def display_edit_user(user_id):
    """displays edit page for specified user."""
    user = User.query.get_or_404(user_id)
    name = user.make_full_name
    return render_template("edit_user.html", user=user, name=name)


@app.route("/users/<user_id>/edit", methods=["POST"])
def commit_edit_user(user_id):
    """confirms edit choices from form and commits to db."""

    # collect user and form data to prepare update.
    user = User.query.get_or_404(user_id)
    new_fname = request.form['f_name']
    new_lname = request.form['l_name']
    new_img_url = request.form['new_img_url']

    # change instant data using data from form.
    user.first_name = new_fname
    user.last_name = new_lname
    user.image_url = new_img_url

    #commit to db
    db.session.commit()

    return redirect(f'/users/{user_id}/edit')


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """deletes user record from db and returns to users list"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/')

# *********** Part Two Post routes *************

@app.route('/posts/<post_id>')
def display_unique_post(post_id):
    """displays unique post based on post_id ((Hyperlink))"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)
    return render_template("post.html", post=post, user=user)

@app.route('/users/<user_id>/posts/new')
def display_new_post_form(user_id):
    """shows form for user to write new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=["POST"])
def save_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, 
                    content=content, 
                    user_id=user.id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>/edit')
def show_post_edit(post_id):
    """displays edit form for unique post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)
    return render_template("edit_post.html", post=post, user=user)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def confirm_post_edit(post_id):
    """updates db with post edit"""
    post = Post.query.get_or_404(post_id)
    new_title = request.form['title']
    new_content = request.form['content']

    post.title = new_title
    post.content = new_content

    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """deletes given post and commits to db."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route('/tags')
def display_all_tags():
    """displays list of all tags."""

    tags = Tag.query.all()

    return render_template("tags_list.html", tags=tags)

@app.route("/tags/<tag_id>")
def display_unique_tag(tag_id):
    """shows infor for individual tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("show_tag.html", tag=tag)

@app.route('/tags/new', methods=["GET", "POST"])
def add_new_tag():
    """display form to add new tag. or POSTS new data to db from form."""
    if (request.method == "POST"):
        name = request.form['t_name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        return redirect('/tags')

    else:
        return render_template("new_tag.html")
    
@app.route('/tags/<tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """handles get and post request to edit tag info"""
    if (request.method == "POST"):
        tag = Tag.query.get_or_404(tag_id)
        new_name = request.form['t_name']

        tag.name = new_name

        db.session.commit()

        return redirect(f'/tags/{tag.id}/edit')
    
    else:
        tag = Tag.query.get_or_404(tag_id)

        return render_template('edit_tag.html', tag=tag)
    
@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """deletes proper tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')