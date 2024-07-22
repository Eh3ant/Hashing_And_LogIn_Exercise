from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField,EmailField,TextAreaField
from wtforms.validators import Email,InputRequired,Length


class UserForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password",validators=[InputRequired()])
    email = EmailField("Email",validators=[InputRequired(), Email(),Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",validators=[InputRequired(),Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])    
    
