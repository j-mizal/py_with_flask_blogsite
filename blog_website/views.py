from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User 
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all() 

    return render_template("home.html",  user=current_user, posts=posts)

@views.route("/post-blog", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('Sorry, post cannot be blank.', category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Successfully posted a blog!', category="success")
            return redirect(url_for('views.home'))
            
    return render_template('createpost.html', user=current_user)

@views.route("/delete-blog/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('Permission denied. You cannot delete the post.', category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Sorry, user not found.', category='error')
        return redirect(url_for('views.home'))
 
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)


