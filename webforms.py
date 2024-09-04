from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired, EqualTo, Length

class EditUserForm(FlaskForm):
    username = StringField("Votre pseudo", validators=[InputRequired(), Length(3,20)])
    email = StringField("Votre email", validators=[InputRequired(), Email()])
    submit = SubmitField("Confirmer")


class SignUpForm(EditUserForm):
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


class LogInForm(FlaskForm):
    email = StringField("Votre email", validators=[InputRequired(), Email()])
    password = PasswordField('Votre mot de passe',
                             validators=[InputRequired()])
    submit = SubmitField("Se connecter")


class PostForm(FlaskForm):
    title = StringField("Titre", validators=[InputRequired()])
    content = TextAreaField("Contenu", validators=[InputRequired()])
    submit = SubmitField("Confirmer")