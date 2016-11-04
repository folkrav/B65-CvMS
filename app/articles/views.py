from flask import render_template, url_for, flash
from . import articles
from app.models import Article, ArticleStatus, ArticleCategory
from app import POSTS_PER_PAGE


@articles.route('/<string:category>')
@articles.route('/<string:category>/<int:page>')
def articles(category, page=1):
    posts = Article.query.filter_by(category=ArticleCategory.query.get(ArticleCategory.categories[category]))
    posts = posts.filter_by(status=ArticleStatus.query.get(ArticleStatus.PUBLISHED))
    posts = posts.order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('articles/article.html', posts=posts)
