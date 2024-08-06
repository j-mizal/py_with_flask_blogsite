from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment 
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
 
    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.')
    else:
        post = Post.query.filter_by(id = post_id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', category='success')
        else:
            flash('Cannot locate post.', category='error')
    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('Permission denied.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))