from .__init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


users_privileges = db.Table('users_privileges', db.Model.metadata,
    db.Column('id_privilege', db.Integer, db.ForeignKey('privilege_groups.id_privilege')),
    db.Column('id_user', db.Integer, db.ForeignKey('users.id_user'))
)


article_collaborators = db.Table('article_collaborators', db.Model.metadata,
    db.Column('id_article', db.Integer, db.ForeignKey('articles.id_article')),
    db.Column('id_collaborator', db.Integer, db.ForeignKey('users.id_user'))
)


article_tags = db.Table('article_tags', db.Model.metadata,
    db.Column('id_article', db.Integer, db.ForeignKey('articles.id_article')),
    db.Column('id_tag', db.Integer, db.ForeignKey('tags.id_tag'))
)


class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime)
    activated = db.Column(db.Boolean, default=False)
    privileges = db.relationship('PrivilegeGroup', secondary=users_privileges)

    def __init__(self, name=None, username=None, email=None, password=None):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('the attribute "Password" is not directly readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PrivilegeGroup(db.Model):
    __tablename__ = 'privilege_groups'
    id_privilege = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(192))


class Article(db.Model):
    __tablename__ = 'articles'
    id_article = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    summary = db.Column(db.String(160))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    collaborators = db.relationship('User', secondary=article_collaborators)
    tags = db.relationship('Tag', secondary=article_tags)
    id_category = db.Column(db.Integer, db.ForeignKey('article_categories.id_category'))
    category = db.relationship('ArticleCategory', backref=db.backref('articles', lazy='dynamic'))
    id_status = db.Column(db.Integer, db.ForeignKey('article_statuses.id_status'))
    status = db.relationship('ArticleStatus', backref=db.backref('articles', lazy='dynamic'))


class Tag(db.Model):
    __tablename__ = 'tags'
    id_tag = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))


class ArticleStatus(db.Model):
    __tablename__ = 'article_statuses'
    id_status = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))


class ArticleCategory(db.Model):
    __tablename__ = 'article_categories'
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(160))

