from . import users
from app.models import User, PrivilegeGroup
from flask import render_template, abort
from decorators import privileges_required


@users.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('users/user.html', user=user)
