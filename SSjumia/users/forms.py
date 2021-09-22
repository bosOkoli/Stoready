from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,HiddenField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length, ValidationError
from SSjumia.models import User



class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email= StringField("Email",validators=[DataRequired(),Email()])
    first_name=StringField('First Name',validators=[DataRequired()])
    last_name=StringField('Last Name',validators=[DataRequired()])
    phone_num=IntegerField('Phone Number',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    address=StringField('Address',validators=[DataRequired()])
    city=StringField('City',validators=[DataRequired()])
    state=SelectField('State',validators=[DataRequired()],
                            choices=[('abia','Abia'),('adamawa','Adamawa'),('akwa-ibom','Akwa-Ibom'),('anambra','Anambra'),('bauchi','Bauchi'),('bayelsa','Bayelsa',),('benue','Benue'),('borno','Borno'),
                            ('cross-river','Cross River'),('delta','Delta'),('ebonyi','Ebonyi'),('edo','Edo'),('ekiti','Ekiti'),('enugu','Enugu'),('gombe','Gombe'),('imo','Imo'),('jigawa','Jigawa'),
                            ('kaduna','Kaduna'),('kano','Kano'),('kastina','Kastina'),('kebbi','Kebbi'),('kogi','Kogi'),('kwara','Kwara'),('lagos','Lagos'),('nasarawa','Nasarawa'),('niger','Niger'),
                            ('ondo','Ondo'),('osun','Osun'),('oyo','Oyo'),('plateau','Plateau'),('rivers','Rivers'),('sokoto','Sokoto'),('taraba','Taraba'),('yobe','Yobe'),('zamfara','Zamfara'),('abuja','Abuja')])
    country=SelectField('Country',validators=[DataRequired()],choices=('nigeria','Nigeria'))
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def username_validation(self,username):
        user=User.query.filter_by(username=username).first()
        if user:
            raise ValidationError('Username has been taken. Please choose a different one')



class LoginForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Log In')
    
class AddToCart(FlaskForm):
    quantity=IntegerField('Quantity',validators=[DataRequired()])
    product_id=HiddenField('ID',validators=[DataRequired()])

class OrderForm(FlaskForm):
    reference=StringField('Reference',validators=[DataRequired()])
   
    payment_type=SelectField('Payment Type',validators=[DataRequired()],choices=[('cash on delivery','Cash On Delivery'),('card','Card')])





