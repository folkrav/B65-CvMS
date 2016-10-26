from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[Required('Veuillez entrer un nom d\'utilisateur'),
                                                             Length(1,64)])
    password = PasswordField('Mot de passe', validators=[Required('Veuillez entrer un mot de passe.')])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Me connecter')

class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[Required('Veuillez entrer un nom d\'utilisateur'), Length(1,64),
                                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                             'Un nom d\'usager ne peut contenir que des lettres, '
                                                             'chiffres, points ou barres de soulignement.')])
    name = StringField('Nom', validators=[Length(1,128)])
    email = StringField('Courriel', validators=[Required('Veuillez entrer un courriel.'),
                                                Length(1,128),
                                                Email(message='Ce courriel est invalide.')])
    password = PasswordField('Mot de passe', validators=[Required('Veuillez entrer un mot de passe.')])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[Required('Veuillez confirmer le mot de passe.'),
                                                                              EqualTo('password', message='Les mots de passe de concordent pas!')])
    submit = SubmitField('Créer mon compte')

    def validate_email(self, field):
        from ...models import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Courriel déjà utilisé.')
    
    def validate_username(self, field):
        from ...models import User
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Nom d\'utilisateur déjà utilisé.')
