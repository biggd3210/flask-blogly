"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'thisshouldbesomethingelse'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

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
    name = user.make_full_name()
    return render_template("user_page.html", user=user, name=name)

@app.route("/users/<int:user_id>/edit")
def display_edit_user(user_id):
    """displays edit page for specified user."""
    user = User.query.get_or_404(user_id)
    name = user.make_full_name()
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