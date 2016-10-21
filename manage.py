#!./venv/bin/python3
import os
from app import create_app, db
from app.models import User, PrivilegeGroup, Article, Tag, ArticleCategory, ArticleStatus
from flask_script import Manager, Shell

app = create_app('default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)  # to add when migration is written

@manager.command
def test():
    """Runs all the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
