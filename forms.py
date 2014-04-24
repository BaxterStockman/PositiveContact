from wtforms import Form, FileField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp


class SimpleForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')


class ContactForm(Form):
    fname = StringField('First name', [InputRequired()])
    lname = StringField('Last name', [InputRequired()])
    email = StringField('Email', [Email()])
    phone = StringField('Phone number', [Regexp('\d{3}\D*\d{3}\D*\d{4}\D*\d*')])
    # photo = FileField('Photo')


class LoginForm(Form):
    email = StringField('Email', [Email()])
    password = PasswordField('Password', [InputRequired()])


class SignupForm(Form):
    email = StringField('Email', [Email()])
    password = PasswordField('Password', [InputRequired()])
    confirm = PasswordField(
        'Password', [InputRequired(),
                     EqualTo('password', message="Passwords must match")])
