from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class ProductForm(FlaskForm):
    name = StringField('Nume Produs', validators=[InputRequired()])
    price = FloatField('Preț', validators=[InputRequired()])
    description = TextAreaField('Descriere')
    image = FileField('Imagine Produs', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Doar imagini sunt permise!')
    ])
    submit = SubmitField('Adaugă Produs')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=8), EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')
    
class AddToCartForm(FlaskForm):
    submit = SubmitField('Adaugă în coș')