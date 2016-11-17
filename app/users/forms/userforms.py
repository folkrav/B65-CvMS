from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from flask_pagedown.fields import PageDownField
from wtforms.validators import Length, Required
from wtforms import ValidationError


class EditForm(FlaskForm):
    name = StringField('Nom', validators=[Length(1,128)])
    about = PageDownField('À propos')
    location = StringField('Emplacement', validators=[Length(1,128)])
    password = PasswordField('Confirmez votre mot de passe', validators=[Required('Veuillez entrer un mot de passe.')])
    submit = SubmitField('Modifier mes informations')
