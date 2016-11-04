from flask import render_template, url_for, flash
from . import articles
from app.models import Article, ArticleStatus
from app import POSTS_PER_PAGE


@articles.route('/text')
def text(page=1):
    posts = Article.query.order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, True)
    return render_template('articles/text.html', posts=posts)
