from . import main
from app.models import User, PrivilegeGroup
from flask import render_template
from decorators import privileges_required


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')
