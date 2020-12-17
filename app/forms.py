from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import \
    (BooleanField, StringField, PasswordField, SubmitField, TextAreaField,
     RadioField, SelectField, DateField)
from wtforms.validators import \
    (DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired)
from app.models import User


__all__ = (
    'RegistrationForm', 'LoginForm', 'UpdateForm', 'CustomerForm',

)


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        Length(min=2, max=25, message='Must be between 2 and 25 characters long')])  # , Regexp(r'[\u4e00-\u9fa5]') chinese only
    account = StringField('Account', validators=[
        Length(min=7, max=25, message='Must be between 7 and 25 characters long'),
        Regexp(r'^[A-Za-z]+[A-Za-z0-9]+$')])
    email = StringField('Email Address', validators=[Length(min=6, max=35), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Regexp(r'^\D+[A-Za-z0-9@#$%^&+=_]{7,}',
                               message='At least 8 characters long')])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), Regexp(r'^\D+[A-Za-z0-9@#$%^&+=_]{7,}'),
        EqualTo('password', message='Password must match')])
    submit = SubmitField('Sign Up')

    def validate_account(self, account):
        pattern = User.query.filter_by(account=account.data).first()
        if pattern: raise ValidationError(f'[ {pattern.account} ] already exist')

    def validate_email(self, email):
        pattern = User.query.filter_by(email=email.data).first()
        if pattern: raise ValidationError(f'[ {pattern.email} ] has been used')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# todo 待修正


class UpdateForm(FlaskForm):
    file_type = ['jpg', 'png']
    username = StringField('Username', validators=[Length(min=4, max=25), Regexp(r'^[A-Za-z]+[A-Za-z0-9]+$')])
    # email = StringField('Email Address', validators=[Length(min=6, max=35), Email()])
    image = FileField('Change selfie', validators=[FileAllowed(file_type)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            data = User.query.filter_by(username=username.data).first()
            if data: raise ValidationError(f'[{username.data}] already in use')
        else: raise ValidationError(f'Same value [{username.data}]--[{current_user.username}]')  # todo 邏輯、文字待修

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         email = User.query.filter_by(email=email.data).first()
    #         if email: raise ValidationError(f'[{email.data}] has been used')


# core from
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact Information', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    birthday = DateField('Birthday', validators=[DataRequired()])
    remark = TextAreaField('Remark')
    submit = SubmitField('Create Customer')


