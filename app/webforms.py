from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired, EqualTo, Length, ValidationError
from app.models import User


class EditUserForm(FlaskForm):
    username = StringField("Votre pseudo", validators=[
                           InputRequired(), Length(max=20)])
    email = StringField("Votre email", validators=[InputRequired(), Email()])
    submit = SubmitField("Confirmer")

    def __init__(self, current_user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_username = current_user.username
        self.original_email = current_user.email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Cet email est déjà utilisé. Veuillez en choisir un autre.')


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Mot de passe actuel', validators=[InputRequired()])
    password = PasswordField(
        'Modifier le mot de passe',
        validators=[
            InputRequired(),
            EqualTo('confirm', message="Les mots de passe doivent correspondre")
        ])
    confirm = PasswordField(
        'Confirmer le nouveau mot de passe', validators=[InputRequired()])
    submit = SubmitField('Mettre à jour le mot de passe')

    def validate_old_password(self, old_password):
        user = User.query.filter_by(id=current_user.id).first()
        if not user.verify_password(old_password.data):
            raise ValidationError('Le mot de passe actuel est incorrect.')


class SignUpForm(FlaskForm):
    username = StringField("Votre pseudo", validators=[
                           InputRequired(), Length(max=20)])
    email = StringField("Votre email", validators=[InputRequired(), Email()])
    password = PasswordField(
        'Votre mot de passe',
        validators=[
            InputRequired(),
            EqualTo('confirm', message="Les mots de passe doivent correspondre")
        ])
    confirm = PasswordField(
        'Confirmer le mot de passe',
        validators=[InputRequired()]
    )
    submit = SubmitField("Créer votre compte")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        if email.errors:
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Cet email est déjà utilisé. Veuillez en renseigner un autre.')


class LogInForm(FlaskForm):
    email = StringField("Votre email", validators=[InputRequired(), Email()])
    password = PasswordField('Votre mot de passe',
                             validators=[InputRequired()])
    submit = SubmitField("Se connecter")

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, email):
        if email.errors:
            return
        self.user = User.query.filter_by(email=email.data).first()
        if not self.user:
            raise ValidationError('Identifiant inconnu')

    def validate_password(self, password):
        if self.user and not self.user.verify_password(password.data):
            raise ValidationError('Mot de passe incorrect')


class PostForm(FlaskForm):
    title = StringField("Titre", validators=[InputRequired()])
    content = TextAreaField("Contenu", validators=[InputRequired()])
    submit = SubmitField("Confirmer")

# ------ Admin Forms ---------
class CreateUserForm(FlaskForm):
    username = StringField("Pseudo", validators=[
                           InputRequired(), Length(max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        'Mot de passe',
        validators=[
            InputRequired(),
            EqualTo('confirm', message="Les mots de passe doivent correspondre")
        ])
    confirm = PasswordField(
        'Confirmer le mot de passe',
        validators=[InputRequired()]
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        if email.errors:
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Cet email est déjà utilisé. Veuillez en renseigner un autre.')

