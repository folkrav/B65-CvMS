from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from flask_pagedown.fields import PageDownField
from wtforms.validators import Length, Email, Required
from wtforms import ValidationError


class EditForm(FlaskForm):
    email = StringField('Courriel', validators=[Length(1,128),
                                                Email(message='Ce courriel est invalide.')])
    about = PageDownField('À propos')
    location = StringField('Emplacement', validators=[Length(1,128)])
    password = PasswordField('Confirmez votre mot de passe', validators=[Required('Veuillez entrer un mot de passe.')])
    submit = SubmitField('Modifier mes informations')
