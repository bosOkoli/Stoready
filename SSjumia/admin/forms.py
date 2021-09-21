from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField,BooleanField,IntegerField,SubmitField
from wtforms import validators
from wtforms.fields.core import SelectField
from wtforms.validators import  DataRequired,Email,EqualTo,ValidationError,Length
from SSjumia.models import User
from flask_wtf.file import FileField, FileAllowed


class AdminRegistrationForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=5,max=20)])
    email= StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    role=SelectField('Role',validators=[DataRequired()],choices=[('administrator','Administrator'),('editor','Editor')])
    submit=SubmitField('Sign Up')

    def username_validation(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has been taken. Please choose a different one!')

    def email_validation(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has been used for another account. Log in if you are the one!')

class AdminLoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Log In')


class AdminUploadForm(FlaskForm):
    Prod_name=StringField('Product Name',validators=[DataRequired(),Length(min=2,max=25)])
    prod_desc=TextAreaField('Description',DataRequired())
    prod_price=IntegerField('Price')
    prod_stock=IntegerField('Stock')
    image_file=FileField('Product Image',validators=[FileAllowed('jpg,png')])
    category=SelectField('Select Category',choices=[('electronics','Electronics'),('food','Food'),('fashion','Fashion'),('health','Health'),('household','Household'),('toletries','Toletries')])


class CompletedOrdersForm(FlaskForm):
    complete_orders=BooleanField('Complete Order')
    
    