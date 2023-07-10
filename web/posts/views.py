"""contains the routes for the blog page"""

from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from web.posts.forms import PostForm
from web import db
from web.models import Post

posts = Blueprint('posts', __name__)

@posts.route("/blog")
def blog():
    """display all blogs, two per page"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('blog.html', posts=posts)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """create a new blog post"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('posts.blog'))
    return render_template("create_post.html", title="New Post", form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    """access a particular post, to get options like edit or delete"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """update a post. prepopulate the post only allowed for the post creator"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':    
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend = "Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """option to delete a post. only allowed for the post creator"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect(url_for('posts.blog'))