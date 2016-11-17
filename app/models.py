from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin


users_privileges = db.Table('users_privileges', db.Model.metadata,
    db.Column('id_privilege', db.Integer, db.ForeignKey('privilege_groups.id')),
    db.Column('id_user', db.Integer, db.ForeignKey('users.id'))
)


article_collaborators = db.Table('article_collaborators', db.Model.metadata,
    db.Column('id_article', db.Integer, db.ForeignKey('articles.id')),
    db.Column('id_collaborator', db.Integer, db.ForeignKey('users.id'))
)


article_tags = db.Table('article_tags', db.Model.metadata,
    db.Column('id_article', db.Integer, db.ForeignKey('articles.id')),
    db.Column('id_tag', db.Integer, db.ForeignKey('tags.id'))
)


class PrivilegeGroup(db.Model):
    __tablename__ = 'privilege_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(192))

    AUTHENTICATED = 1
    CREATOR = 2
    MODERATOR = 3
    ADMINISTRATOR = 4


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    about = db.Column(db.Text)
    location = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime)
    activated = db.Column(db.Boolean, default=True)
    privileges = db.relationship('PrivilegeGroup', secondary=users_privileges)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.privileges is None:
            self.privileges.append(PrivilegeGroup.get(PrivilegeGroup.AUTHENTICATED))

    def can(self, privilege):
        return PrivilegeGroup.query.get(privilege) in self.privileges

    def has_been_seen(self):
        self.last_visit = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('the attribute "Password" is not directly readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    summary = db.Column(db.String(160))
    body = db.Column(db.Text)
    image_path = db.Column(db.String(2083))
    link_url = db.Column(db.String(2083))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    collaborators = db.relationship('User', secondary=article_collaborators)
    tags = db.relationship('Tag', secondary=article_tags)
    id_category = db.Column(db.Integer, db.ForeignKey('article_categories.id'))
    category = db.relationship('ArticleCategory', backref=db.backref('articles', lazy='dynamic'))
    id_status = db.Column(db.Integer, db.ForeignKey('article_statuses.id'))
    status = db.relationship('ArticleStatus', backref=db.backref('articles', lazy='dynamic'))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))


class ArticleStatus(db.Model):
    __tablename__ = 'article_statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))

    DRAFT = 1
    PUBLISHED = 2


class ArticleCategory(db.Model):
    __tablename__ = 'article_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))

    categories = {
        'articles': 1,
        'images': 2,
        'videos': 3
    }


from app import login
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser
