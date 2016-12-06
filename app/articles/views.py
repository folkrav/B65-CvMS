from flask import render_template, url_for, flash, abort, redirect, request
from flask_login import login_required, current_user
from . import articles
from app.models import Article, ArticleStatus, ArticleCategory, PrivilegeGroup, Tag
from app import POSTS_PER_PAGE, db
from .forms.articleforms import TextPublicationForm, ImagePublicationForm, LinkPublicationForm
from decorators import privileges_required


@articles.route('/<string:category>')
@articles.route('/<string:category>/<int:page>')
def articlespage(category, page=1):
    title = category.title()
    posts = Article.query.filter_by(category=ArticleCategory.query.get(ArticleCategory.categories[category]))
    posts = posts.filter_by(status=ArticleStatus.query.get(ArticleStatus.PUBLISHED))
    posts = posts.order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('articles/article.html', posts=posts, title=title)


@articles.route('/<string:category>/new', methods=['GET', 'POST'])
@login_required
@privileges_required(PrivilegeGroup.CREATOR)
def newarticle(category):
    if category not in ArticleCategory.categories.keys():
        abort(404)

    CATEGORIES_FORMS = [TextPublicationForm(), ImagePublicationForm(), LinkPublicationForm()]
    form = CATEGORIES_FORMS[ArticleCategory.categories[category] - 1]
    is_text_article = (category == "articles")

    form.tags.choices = [(str(t.id), t.name) for t in Tag.query.all()]
    form.tags.default = []
    form.tags.process(request.form)

    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          summary=form.summary.data)
        _article_submit(form, article, category)
        redirect(url_for('users.user', username=current_user.username))

    return render_template('articles/newarticle.html', form=form, is_text_article=is_text_article)


@articles.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@privileges_required(PrivilegeGroup.CREATOR)
def editarticle(id):
    article = Article.query.get(id)
    if not article:
        abort(404)

    CATEGORIES_FORMS = [TextPublicationForm(), ImagePublicationForm(), LinkPublicationForm()]
    form = CATEGORIES_FORMS[article.category.id - 1]
    form.title.data = article.title
    form.summary.data = article.summary
    form.status.data = (article.status == ArticleStatus.query.get(ArticleStatus.PUBLISHED))
    is_text_article = (article.category.name == "post")

    tags_choices_all, tags_choices = _get_tags_choices(article)
    form.tags.choices = tags_choices_all
    form.tags.default = [id for id, title in tags_choices]
    form.tags.process(request.form)

    if article.category.name == "post":
        form.body.data = article.body
    elif article.category.name == "image":
        pass
    elif article.category.name == "video":
        pass

    _update_tags(request, article, form)

    if form.validate_on_submit():
        _article_submit(form, article, article.category.name)

    return render_template('articles/newarticle.html', form=form, is_text_article=is_text_article)

def _update_tags(request, article, form):
    tags_choices_all, tags_choices = _get_tags_choices(article)
    tags_choices_dict = dict(tags_choices)
    tags_choices_new = []
    for v in request.form.getlist('tags'):
        if (
                v and
                re.match(r'^[A-Za-z0-9_\- ]+$', v) and
                not(v in tags_choices_dict)):
            tags_choices_new.append((v, v))

    form.tags.choices = tags_choices_all + tags_choices_new
    form.tags.default = [id for id, title in tags_choices]
    form.tags.process(request.form)

def _article_submit(form, article, category):
    article.category = (ArticleCategory.query.get(ArticleCategory.categories[category]))
    article.collaborators.append(current_user)
    article.status = (ArticleStatus.query.get(ArticleStatus.PUBLISHED if form.status.data else ArticleStatus.DRAFT))
    if category == "post":
        article.body = form.body.data
    elif category == "image":
        pass
    elif category == "video":
        pass

    db.session.add(article)
    db.session.commit()

def _get_tags_choices(article):
    all_choices = [(str(t.id), t.name) for t in Tag.query.all()]
    choices = [(t.id, t.name) for t in article.tags]

    return (all_choices, choices)
