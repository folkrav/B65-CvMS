from . import main
from ..models import *


@main.route('/')
@main.route('/index')
def index():
    return '<p>Hello world.</p>'
