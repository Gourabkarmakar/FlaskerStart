from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


class Post_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Password",
                                  validators=[
                                      DataRequired(),
                                      EqualTo('password_hash2',
                                              message="Passwords Must Match! ")
                                  ])
    password_hash2 = PasswordField("Confirm Password",
                                   validators=[DataRequired()])
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField("What Is Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    email = StringField("What is your Email", validators=[DataRequired()])
    password_hash = PasswordField("What is Your Passwords",
                                  validators=[DataRequired()])
    submit = SubmitField("Check")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")
