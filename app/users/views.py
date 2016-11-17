from . import users
from app.models import User
from flask import render_template, abort, flash, redirect, url_for
from flask_login import current_user, login_required
from decorators import privileges_required
from .forms.userforms import EditForm
from app.models import User
from app import db


@users.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('users/user.html', user=user)

@users.route('/<username>/edit', methods=['GET', 'POST'])
def edit(username):
    user = User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)
    form = EditForm(obj=user)

    if form.validate_on_submit():
        if user.check_password(form.password.data):
            user.name = form.name.data
            user.location = form.location.data
            user.about = form.about.data
            db.session.commit()
            flash('Compte modifié.', 'info')
            return redirect(url_for('users.user', username=user.username))
        flash('Mot de passe invalide.', 'warning')
    return render_template('users/edit.html', user=user, form=form)
