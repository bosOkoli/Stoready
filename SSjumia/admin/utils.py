from SSjumia.users.routes import *
from SSjumia.models import Product
import os
import secrets
from PIL import Image
from flask import current_app


def handle_cart():
    products=[]
    grand_total=0
    index=0
    quantity_total=0
    for item in session['cart']:
        product=Product.query.filter_by(id=item['id']).first()   
        quantity=int(item['quantity'])
        total=quantity*product.price
        grand_total+=total
        grand_total_plus_shipping=grand_total + 2000
        products.append({'id':product.id,'name':product.name,'price':product.price,'image':product.image_file,'quantity':quantity,'total':total,'index':index})
        index+=1
        quantity_total+=quantity
        
        return total,grand_total ,grand_total_plus_shipping,quantity_total

def save_upload_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/img2/', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    
    return ('img/img2/' + picture_fn)


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return ('img/profile_pics/' + picture_fn)