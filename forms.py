from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, equal_to
from flask_wtf.file import FileAllowed
from ext import db
from models import User

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(max=50)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')
    
class Register_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), equal_to('password')])
    img = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    register = SubmitField('Register')
    
    def validate_username(self, username):
        user = db.session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose a different username.")
    
class Login_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    login = SubmitField('Login')