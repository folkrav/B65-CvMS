#!./venv/bin/python3
import os
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell, Command, Option
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

class InitDb(Command):
    """Creates the database tables and initial data."""

    def __init__(self, default_name='admin', default_username='admin', default_password='admin',
                 default_email='fake@example.com', default_about='The site administrator', default_location='The Internet'):
        self.default_name=default_name
        self.default_username=default_username
        self.default_email=default_email
        self.default_password=default_password
        self.default_about=default_about
        self.default_location=default_location

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
            Option('-u', '--username', dest='username', default=self.default_username),
            Option('-e', '--email', dest='email', default=self.default_email),
            Option('-p', '--password', dest='password', default=self.default_password),
            Option('-a', '--about', dest='about', default=self.default_about),
            Option('-l', '--location', dest='location', default=self.default_location)
        ]

    def run(self, name, username, email, password, about, location):
        db.create_all()

        # Create the initial database data
        category = [
            ArticleCategory(name='post', description='A text-based post.'),
            ArticleCategory(name='image', description='An image upload.'),
            ArticleCategory(name='video', description='A video link (Youtube, etc.)')
        ]
        status = [
            ArticleStatus(name='draft', description='Unpublished, in the works.'),
            ArticleStatus(name='published', description='Article has been published')
        ]
        priv_group = [
            PrivilegeGroup(name='authenticated', description='Can comment publications and modify his profile.'),
            PrivilegeGroup(name='creator', description='Can publish content on the website.'),
            PrivilegeGroup(name='moderator', description='Can remove or modify any article.'),
            PrivilegeGroup(name='administrator', description='Can activate, remove or modify any user.')
        ]

        # Create user with full administrative rights
        administrator = User(name=name, username=username, email=email,
                             password=password, about=about, location=location)
        administrator.privileges = priv_group

        # Add the data
        db.session.add_all(category)
        db.session.add_all(status)
        db.session.add_all(priv_group)
        db.session.add(administrator)
        db.session.commit()


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('initdb', InitDb)

@manager.command
def test():
    """Runs all the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
