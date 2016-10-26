from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms.authforms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from ..models import User
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('main.index'))
        flash('Mauvaises informations de connection.')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        from ..models import User
        user = User(username=form.username.data, name=form.name.data,
                    email=form.email.data, password=form.password.data)
        from app import db
        db.session.add(user)
        flash('Vous pouvez maintenant vous connecter.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.')
    return redirect(url_for('main.index'))
