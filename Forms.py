from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField, IntegerField,TextAreaField, SelectField
from wtforms.validators import DataRequired, Email,NumberRange

class Registration(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email(),DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Correct password", validators=[DataRequired()])
    submit = SubmitField()

class Autorization(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("remember me ")
    submit = SubmitField("Submit")

class reviewForm(FlaskForm):
   text = TextAreaField("Залишити рецензію: ", validators=[DataRequired()])
   grade = IntegerField("Оцінка: ", validators=[NumberRange(1, 10),DataRequired()])
   submit = SubmitField("Submit")

class searchForm(FlaskForm):
    text = StringField("Поиск:")
    ganreuse = BooleanField("")
    ganre = SelectField ("Поиск:")
    typeuse = BooleanField("")
    type = SelectField ("Поиск:")
    statususe = BooleanField("")
    status = SelectField ("Поиск:")
    agerateuse = BooleanField("")
    agerate = SelectField ("Поиск:")

class CheckboxForm(FlaskForm):
    status = SelectField("")

class ChangeProfileForm(FlaskForm):
    username = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email(),DataRequired()])
    avatar = StringField("Avatar:")
    password = StringField("Password:", validators=[DataRequired()])
    about = StringField("About:")
    submit = SubmitField("Submit")