from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms import ValidationError, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from webapp.models import Users


class PicturesForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=64)])
    description = TextAreaField(
        'Description', [
            DataRequired(),
            Length(min=4, max=240, message='Your message has got wrong length.')])
    file = FileField()
    submit = SubmitField('Submit')

class UsersForm(FlaskForm):
    login = StringField('Login', [DataRequired(), Length(max=64)])
    password = TextAreaField(
        'Password', [
            DataRequired(),
            Length(min=4, max=240, message='Your message has got wrong length.')])
    nickname = TextAreaField(
        'nickname', [
            DataRequired(),
            Length(min=4, max=240, message='Your message has got wrong length.')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class UploadForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=64)])
    submit = SubmitField('Submit')

class СommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')