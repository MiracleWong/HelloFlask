# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


# 4.4.3 custom validationError
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number: ')
    submit = SubmitField()

    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError("Must be 42")


# 4.4.2 upload form
class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[
                      FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


# 4.4.4
class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()


# 4.4.5
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

# 4.4.6


class NewPostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')
