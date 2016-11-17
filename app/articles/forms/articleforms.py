from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FileField, HiddenField
from flask_pagedown.fields import PageDownField
from wtforms.validators import Length, Required
from wtforms import ValidationError


class NewArticleForm(FlaskForm):
    title = StringField('Titre', validators=[Length(1,64), Required('Veuillez entrer un titre.')])
    summary = StringField('Résumé', validators=[Length(1,160),
                                               Required('Veuillez entrer une courte description votre publication.')])
    status = BooleanField('Publier l\'article immédiatement')
    submit = SubmitField('Enregistrer les modifications')
    category = HiddenField()


class TextPublicationForm(NewArticleForm):
    body = PageDownField('Texte complet de l\'article', validators=[Required('Veuillez entrer du contenu.')])


class ImagePublicationForm(NewArticleForm):
    body = FileField('Téléverser une image', validators=[Required('Veuillez ajouter une image.')])


class LinkPublicationForm(NewArticleForm):
    body = StringField('URL', validators=[Length(1,64), Required('Veuillez entrer un titre.')])
