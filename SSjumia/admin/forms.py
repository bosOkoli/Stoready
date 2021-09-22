from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,IntegerField,SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import  DataRequired,Length
from SSjumia.models import User
from flask_wtf.file import FileField, FileAllowed

class AdminUploadForm(FlaskForm):
    prod_name=StringField('Product Name',validators=[DataRequired(),Length(min=2,max=25)])
    product_desc=TextAreaField('Description',validators=[DataRequired(),Length(min=10,max=100)])
    prod_price=IntegerField('Price')
    prod_stock=IntegerField('Stock')
    image_file=FileField('Product Image',validators=[FileAllowed(['jpg','png'])])
    category=SelectField('Select Category',choices=[('electronics','Electronics'),('food','Food'),('fashion','Fashion'),('health','Health'),('household','Household'),('toletries','Toletries')])
    submit=SubmitField('Upload Product')

class CompletedOrdersForm(FlaskForm):
    complete_orders=BooleanField('Complete Order')
    
    