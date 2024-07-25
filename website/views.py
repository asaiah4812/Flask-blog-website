from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import current_user, login_required
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template('core/index.html', user=current_user)

@views.route("/create-post", methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        if not title or not body:
            flash('Post fields cannot be empty!', category='error')
        else:
            post = Post(title=title, body=body, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully 🙌', category='success')
            return redirect(url_for('views.posts'))

    return render_template('core/create_post.html', user=current_user)

@views.route('/posts', methods=['GET'])
@login_required
def posts():
    posts = Post.query.all()
    return render_template('core/posts.html', posts=posts, user=current_user)

@views.route('/delete-post/<id>')
@login_required
def delete_posts(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted', category='info')
    
    return redirect(url_for('views.posts'))

@views.route('/post/<id>', methods=['GET'])
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.all()
    return render_template('core/post.html', comments=comments, post=post, user=current_user)

@views.route('/create-comment/<post_id>', methods=['POST', 'GET'])
def create_comment(post_id):
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('text input can blank', category='error')
        else:
            post = Post.query.filter_by(id=post_id).first()
            if post:
                comment = Comment(text=text, author=current_user.id, post_id=post_id)
                db.session.add(comment)
                db.session.commit()
        return redirect(url_for('views.post', id=post.id))

@views.route('/delete-comment/<id>')
@login_required
def delete_comments(id):
    comment = Comment.query.filter_by(id=id).first()

    if not post:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Post has been deleted', category='info')
    
    return redirect(url_for('views.post', id=comment.id))

@views.route('/posts/<username>')
@login_required
def user_post(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Hey! No User with that username exists.", category='error')
        return redirect(url_for('views.posts'))
    posts = user.posts
    return render_template("core/user_post.html", posts=posts, user=current_user, username=username)

@views.route('/like-post/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({"likes":len(post.likes)})


