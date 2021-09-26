from operator import contains
from flask import Blueprint
from flask.templating import render_template
from SSjumia.models import Product
from sqlalchemy import desc
from flask import request



main=Blueprint('main',__name__)

@main.route('/')

@main.route('/home')
def home():
    q=request.args.get('q') 
    if q:
        electronics = Product.query.filter_by(cat_id=1).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        food = Product.query.filter_by(cat_id=2).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        fashion = Product.query.filter_by(cat_id=3).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        health = Product.query.filter_by(cat_id=4).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        household = Product.query.filter_by(cat_id=5).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        toiletries = Product.query.filter_by(cat_id=6).filter(Product.prod_name.contains(q) | Product.product_desc.contains(q)).all()
        products=Product.query.filter(Product.prod_name.contains(q) | Product.product_desc.contains(q))
    else:
        products=Product.query.all()
        electronics = Product.query.filter_by(cat_id=1).all()
        food = Product.query.filter_by(cat_id=2).all()
        fashion = Product.query.filter_by(cat_id=3).all()
        health = Product.query.filter_by(cat_id=4).all()
        household = Product.query.filter_by(cat_id=5).all()
        toiletries = Product.query.filter_by(cat_id=6).all()
        trending = Product.query.order_by(desc(Product.id)).all()
    return render_template('main/home.html',title='home',products=products,electronics=electronics,food=food,fashion=fashion,health=health,household=household,toiletries=toiletries)
