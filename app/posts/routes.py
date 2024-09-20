from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.posts import bp
from app.extensions import db
from app.models import Post
from app.webforms import PostForm

@bp.route('/<int:post_id>')
def view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', post=post)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('posts/create.html', form=form)

@bp.route('/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("Vous n'êtes pas autorisé à modifier cet article.", 'danger')
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(url_for('posts.view', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('posts/edit.html', post=post, form=form)


@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("Vous n'êtes pas autorisé à supprimer cet article.", 'danger')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash("L'article a bien été supprimé.", 'success')
    return redirect(url_for('index'))

