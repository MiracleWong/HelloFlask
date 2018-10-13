# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


# 4.4.3 custom validationError
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number: ')
    submit = SubmitField()

    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError("Must be 42")