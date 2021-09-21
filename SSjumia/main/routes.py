from flask import Flask
from flask import Blueprint
from flask.templating import render_template
from SSjumia.models import Product



main=Blueprint('main',__name__)

@main.route('/')

@main.route('/home')
def home():
    products=Product.query.all()
    return render_template('main/home.html',title='home',products=products)
