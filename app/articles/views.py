from flask import render_template, url_for, flash
from . import articles
from app.models import Article, ArticleStatus
from app import POSTS_PER_PAGE


@articles.route('/text')
@articles.route('/text/<int:page>')
def text(page=1):
    posts = Article.query.filter_by(status=ArticleStatus.query.get(ArticleStatus.PUBLISHED)).order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, True)
    return render_template('articles/text.html', posts=posts)
