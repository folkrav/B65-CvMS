from flask import render_template, url_for, flash, abort, redirect, request
from flask_login import login_required, current_user
from . import articles
from app.models import Article, ArticleStatus, ArticleCategory, PrivilegeGroup, Tag
from app import POSTS_PER_PAGE, ALLOWED_EXTENSIONS, UPLOAD_FOLDER, db
from .forms.articleforms import TextPublicationForm, ImagePublicationForm, LinkPublicationForm
from decorators import privileges_required
from werkzeug.utils import secure_filename


@articles.route('/<string:category>')
@articles.route('/<string:category>/<int:page>')
def articlespage(category, page=1):
    title = category.title()
    posts = Article.query.filter_by(category=ArticleCategory.query.get(ArticleCategory.categories[category]))
    posts = posts.filter_by(status=ArticleStatus.query.get(ArticleStatus.PUBLISHED))
    posts = posts.order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('articles/article.html', posts=posts, title=title)

@articles.route('/search')
def search(page=1):
    articles = Article.query.filter(Article.body.match(request.args.get('q'))).order_by(Article.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('articles/article.html', posts=articles, title='Résultats de recherche')

@articles.route('/<int:id>/delete')
def delete(id):
    article = Article.query.get(id)
    if not article:
        abort(404)
    db.session.delete(article)
    db.session.commit()
    flash('Article supprimé!', 'success')
    return redirect(url_for('users.user', username=current_user.username))

@articles.route('/<int:id>/publish')
def publish(id):
    article = Article.query.get(id)
    if not article:
        abort(404)
    article.status = ArticleStatus.query.get(ArticleStatus.PUBLISHED)
    db.session.add(article)
    db.session.commit()
    flash('Article publié!', 'success')
    return redirect(url_for('users.user', username=current_user.username))

@articles.route('/<int:id>/read')
def read(id):
    article = Article.query.get(id)
    if not article:
        abort(404)

    return render_template('articles/read.html', article=article)


@articles.route('/<string:category>/new', methods=['GET', 'POST'])
@login_required
@privileges_required(PrivilegeGroup.CREATOR)
def newarticle(category):
    if category not in ArticleCategory.categories.keys():
        abort(404)

    CATEGORIES_FORMS = [TextPublicationForm(), ImagePublicationForm(), LinkPublicationForm()]
    form = CATEGORIES_FORMS[ArticleCategory.categories[category] - 1]
    is_text_article = (category == "post")

    # form.tags.choices = [(str(t.id), t.name) for t in Tag.query.all()]
    # form.tags.default = []
    # form.tags.process(request.form)

    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          summary=form.summary.data)
        _article_submit(form, article, category)
        flash('Publication créée.', 'success')
        return redirect(url_for('users.user', username=current_user.username))

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

    # tags_choices_all, tags_choices = _get_tags_choices(article)
    # form.tags.choices = tags_choices_all
    # form.tags.default = [id for id, title in tags_choices]
    # form.tags.process(request.form)

    if article.category.name == "post":
        form.body.data = article.body

    if form.validate_on_submit():
        # _update_tags(request, article, form)
        _article_submit(form, article, article.category.name, update=True)
        flash('Article modifié avec succès.', 'success')
        return redirect(url_for('users.user', username=current_user.username))

    return render_template('articles/newarticle.html', form=form, is_text_article=is_text_article)

# def _update_tags(request, article, form):
#     tags_choices_all, tags_choices = _get_tags_choices(article)
#     tags_choices_dict = dict(tags_choices)
#     tags_choices_new = []
#     import re
#     for v in request.form.getlist('tags'):
#         if (
#                 v and
#                 re.match(r'^[A-Za-z0-9_\- ]+$', v) and
#                 not(v in tags_choices_dict)):
#             tags_choices_new.append((v, v))
#
#     form.tags.choices = tags_choices_all + tags_choices_new
#     form.tags.default = [id for id, title in tags_choices]
#     form.tags.process(request.form)

def _article_submit(form, article, category, update=False):
    article.status = (ArticleStatus.query.get(ArticleStatus.PUBLISHED if form.status.data else ArticleStatus.DRAFT))
    article.category = (ArticleCategory.query.get(ArticleCategory.categories[category]))

    if category == "post":
        article.body = form.body.data
    elif category == "image":
        if _allowed_file(form.body.data.filename):
            filename = secure_filename(form.body.data.filename)
            import os
            file_path = os.path.join(UPLOAD_FOLDER, form.title.data)
            form.body.data.save(file_path)
            article.image_path = form.title.data
    elif category == "video":
        from urllib.parse import urlparse, parse_qs
        url = urlparse(form.body.data)
        params = parse_qs(url.query)
        article.link_url = 'https://www.youtube.com/embed/{0}'.format(params["v"][0])

    if not update:
        article.collaborators.append(current_user)
    db.session.add(article)
    db.session.commit()

# def _get_tags_choices(article):
#     all_choices = [(str(t.id), t.name) for t in Tag.query.all()]
#     choices = [(t.id, t.name) for t in article.tags]
#
#     return (all_choices, choices)

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
