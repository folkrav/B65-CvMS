from flask import render_template, url_for, flash, abort, redirect
from flask_login import login_required, current_user
from . import articles
from app.models import Article, ArticleStatus, ArticleCategory, PrivilegeGroup
from app import POSTS_PER_PAGE, db
from .forms.articleforms import TextPublicationForm, ImagePublicationForm, LinkPublicationForm
from decorators import privileges_required


@articles.route('/<string:category>')
@articles.route('/<string:category>/<int:page>')
def articlespage(category, page=1):
    posts = Article.query.filter_by(category=ArticleCategory.query.get(ArticleCategory.categories[category]))
    posts = posts.filter_by(status=ArticleStatus.query.get(ArticleStatus.PUBLISHED))
    posts = posts.order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('articles/article.html', posts=posts)


@articles.route('/new/<string:category>', methods=['GET', 'POST'])
@login_required
@privileges_required(PrivilegeGroup.CREATOR)
def newarticle(category):
    if category not in ArticleCategory.categories.keys():
        abort(404)

    categories_forms = [TextPublicationForm(), ImagePublicationForm(), LinkPublicationForm()]
    form = categories_forms[ArticleCategory.categories[category] - 1]
    is_text_article = (category == "articles")
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          summary=form.summary.data)
        article.category = (ArticleCategory.query.get(ArticleCategory.categories[category]))
        article.collaborators.append(current_user)
        article.status = (ArticleStatus.query.get(ArticleStatus.PUBLISHED if form.status.data else ArticleStatus.DRAFT))
        if category == "articles":
            article.body = form.body.data
        elif category == "images":
            pass
        elif category == "links":
            pass

        db.session.add(article)
        db.session.commit()
        redirect(url_for('users.user', username=current_user.username))


    return render_template('articles/newarticle.html', form=form, is_text_article=is_text_article)
