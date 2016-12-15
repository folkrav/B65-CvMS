from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, SubmitField, HiddenField, SelectMultipleField
from flask_pagedown.fields import PageDownField
from wtforms.validators import Length, Required, URL
from app import ALLOWED_EXTENSIONS


class NewArticleForm(FlaskForm):
    title = StringField('Titre', validators=[Length(1,64), Required('Veuillez entrer un titre.')])
    summary = StringField('Résumé', validators=[Length(1,160),
                                               Required('Veuillez entrer une courte description votre publication.')])
    status = BooleanField('Publier l\'article immédiatement')
    tags = SelectMultipleField('Tags')
    submit = SubmitField('Enregistrer les modifications')
    category = HiddenField()


class TextPublicationForm(NewArticleForm):
    body = PageDownField('Texte complet de l\'article', validators=[Required('Veuillez entrer du contenu.')])


class ImagePublicationForm(NewArticleForm):
    body = FileField('Téléverser une image', validators=[FileRequired(),
                                                         FileAllowed(ALLOWED_EXTENSIONS, 'Images seulement!')])


class LinkPublicationForm(NewArticleForm):
    body = StringField('URL', validators=[Length(1,64),
                                          Required('Veuillez entrer un titre.'),
                                          URL(require_tld=True, message="Veuillez entrer un lien valide.")])
