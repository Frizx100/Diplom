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
    remember = BooleanField("remember me ",validators=[DataRequired()])
    submit = SubmitField("Submit")

class reviewForm(FlaskForm):
   text = TextAreaField("Оставить отзыв: ", validators=[DataRequired()])
   grade = IntegerField("Оценка: ", validators=[NumberRange(0, 10),DataRequired()])
   submit = SubmitField("Submit")

class searchForm(FlaskForm):
    text = StringField("Поиск:")
    ganre = SelectField ("Поиск:")
    type = SelectField ("Поиск:")
    status = SelectField ("Поиск:")
    agerate = SelectField ("Поиск:")